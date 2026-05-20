from dotenv import load_dotenv
load_dotenv()
 
import json
import time
import hashlib
import secrets
import asyncio
import os
from typing import Optional
from contextlib import asynccontextmanager
 
import httpx
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
 
from database import get_db, init_db
from models import (
    RegisterBody, LoginBody, UpdateProfileBody, ChangePasswordBody,
    ConnectBotBody, CheckBotBody,
    ScenarioBody, UpdateScenarioBody,
    WebhookUpdate,
)
from scenario_engine import (
    find_active_scenario, execute_scenario,
    resume_scenario, handle_goto,
)
 
# ─── Keepalive (пинг каждые 10 минут чтобы Render не засыпал) ────────────────
 
SELF_URL = os.getenv("SELF_URL", "")
 
async def _keepalive():
    await asyncio.sleep(60)
    while True:
        try:
            if SELF_URL:
                async with httpx.AsyncClient() as client:
                    await client.get(f"{SELF_URL}/api/health", timeout=10)
                print("[keepalive] ping ok")
        except Exception as e:
            print(f"[keepalive] ping failed: {e}")
        await asyncio.sleep(30)
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(_keepalive())
    yield
    task.cancel()
 
# ─── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="BOTOLABR API", version="2.0.0", lifespan=lifespan)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
security = HTTPBearer()
 
 
# ─── Auth helpers ─────────────────────────────────────────────────────────────
 
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
 
 
def create_token(user_id: int) -> str:
    token = secrets.token_hex(32)
    expires = int(time.time()) + 30 * 24 * 3600
    with get_db() as db:
        db.execute(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (%s, %s, %s)",
            (token, user_id, expires)
        )
    return token
 
 
def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    with get_db() as db:
        db.execute(
            "SELECT user_id FROM sessions WHERE token=%s AND expires_at>%s",
            (token, int(time.time()))
        )
        row = db.fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    with get_db() as db:
        db.execute("SELECT * FROM users WHERE id=%s", (row["user_id"],))
        user = db.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
 
 
# ─── Auth routes ──────────────────────────────────────────────────────────────
 
@app.post("/api/auth/register")
def register(body: RegisterBody):
    if len(body.username) < 3:
        raise HTTPException(400, "Логин должен содержать минимум 3 символа")
    if len(body.password) < 6:
        raise HTTPException(400, "Пароль должен содержать минимум 6 символов")
    with get_db() as db:
        db.execute(
            "SELECT id FROM users WHERE username=%s OR email=%s",
            (body.username, body.email)
        )
        exists = db.fetchone()
        if exists:
            raise HTTPException(400, "Пользователь с таким логином или email уже существует")
        db.execute(
            "INSERT INTO users (username, email, password, created_at) VALUES (%s, %s, %s, %s)",
            (body.username.strip(), body.email.strip(), hash_password(body.password), int(time.time()))
        )
        db.execute("SELECT * FROM users WHERE username=%s", (body.username,))
        user = db.fetchone()
    token = create_token(user["id"])
    return {"token": token, "user": {"id": user["id"], "username": user["username"], "email": user["email"]}}
 
 
@app.post("/api/auth/login")
def login(body: LoginBody):
    with get_db() as db:
        db.execute("SELECT * FROM users WHERE username=%s", (body.username.strip(),))
        user = db.fetchone()
    if not user or user["password"] != hash_password(body.password):
        raise HTTPException(401, "Неверный логин или пароль")
    token = create_token(user["id"])
    return {
        "token": token,
        "user": {"id": user["id"], "username": user["username"], "email": user["email"], "name": user["name"]}
    }
 
 
@app.post("/api/auth/logout")
def logout(creds: HTTPAuthorizationCredentials = Depends(security)):
    with get_db() as db:
        db.execute("DELETE FROM sessions WHERE token=%s", (creds.credentials,))
    return {"ok": True}
 
 
# ─── Profile routes ───────────────────────────────────────────────────────────
 
@app.get("/api/me")
def get_me(user=Depends(get_current_user)):
    return {k: v for k, v in user.items() if k != "password"}
 
 
@app.patch("/api/me")
def update_profile(body: UpdateProfileBody, user=Depends(get_current_user)):
    fields, vals = [], []
    if body.name     is not None: fields.append("name=%s");     vals.append(body.name)
    if body.lastname is not None: fields.append("lastname=%s"); vals.append(body.lastname)
    if body.email    is not None: fields.append("email=%s");    vals.append(body.email)
    if body.username is not None: fields.append("username=%s"); vals.append(body.username)
    if not fields:
        return {"ok": True}
    vals.append(user["id"])
    with get_db() as db:
        db.execute(f"UPDATE users SET {', '.join(fields)} WHERE id=%s", vals)
    return {"ok": True}
 
 
@app.post("/api/me/password")
def change_password(body: ChangePasswordBody, user=Depends(get_current_user)):
    if user["password"] != hash_password(body.current_password):
        raise HTTPException(400, "Неверный текущий пароль")
    if len(body.new_password) < 6:
        raise HTTPException(400, "Пароль должен содержать минимум 6 символов")
    with get_db() as db:
        db.execute(
            "UPDATE users SET password=%s WHERE id=%s",
            (hash_password(body.new_password), user["id"])
        )
    return {"ok": True}
 
 
@app.post("/api/me/avatar-base64")
async def upload_avatar_b64(request: Request, user=Depends(get_current_user)):
    data = await request.json()
    avatar_data = data.get("avatar")
    if not avatar_data:
        raise HTTPException(400, "Нет данных аватара")
    with get_db() as db:
        db.execute("UPDATE users SET avatar=%s WHERE id=%s", (avatar_data, user["id"]))
    return {"ok": True}
 
 
# ─── Bot routes ───────────────────────────────────────────────────────────────
 
@app.get("/api/bots")
def get_bots(user=Depends(get_current_user)):
    with get_db() as db:
        db.execute(
            "SELECT * FROM bots WHERE user_id=%s ORDER BY connected_at DESC",
            (user["id"],)
        )
        bots = db.fetchall()
    return list(bots)
 
 
@app.post("/api/bots/check")
async def check_bot_token(body: CheckBotBody):
    token = body.token.strip()
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://api.telegram.org/bot{token}/getMe",
            timeout=10,
        )
    data = r.json()
    if not data.get("ok"):
        raise HTTPException(400, "Неверный токен Telegram")
    return {
        "ok": True,
        "bot_username": data["result"]["username"],
        "bot_name":     data["result"]["first_name"],
    }
 
 
@app.post("/api/bots")
async def connect_bot(body: ConnectBotBody, user=Depends(get_current_user)):
    token = body.token.strip()
    with get_db() as db:
        db.execute(
            "SELECT id FROM bots WHERE user_id=%s AND token=%s",
            (user["id"], token)
        )
        dup = db.fetchone()
    if dup:
        raise HTTPException(400, "Этот бот уже подключён к вашему аккаунту")
 
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
    tg = r.json()
    if not tg.get("ok"):
        raise HTTPException(400, "Неверный токен Telegram")
 
    bot_username = tg["result"]["username"]
    bot_name     = tg["result"]["first_name"]
 
    with get_db() as db:
        db.execute(
            "INSERT INTO bots (user_id, token, bot_username, bot_name, connected_at) VALUES (%s, %s, %s, %s, %s)",
            (user["id"], token, bot_username, bot_name, int(time.time()))
        )
        bot_id = db.lastrowid
        db.execute("SELECT * FROM bots WHERE id=%s", (bot_id,))
        bot = db.fetchone()
    return dict(bot)
 
 
@app.delete("/api/bots/{bot_id}")
def delete_bot(bot_id: int, user=Depends(get_current_user)):
    with get_db() as db:
        db.execute(
            "SELECT id FROM bots WHERE id=%s AND user_id=%s", (bot_id, user["id"])
        )
        bot = db.fetchone()
        if not bot:
            raise HTTPException(404, "Бот не найден")
        db.execute("DELETE FROM scenarios WHERE bot_id=%s",   (bot_id,))
        db.execute("DELETE FROM user_states WHERE bot_id=%s", (bot_id,))
        db.execute("DELETE FROM bots WHERE id=%s",            (bot_id,))
    return {"ok": True}
 
 
@app.patch("/api/bots/{bot_id}/toggle")
def toggle_bot(bot_id: int, user=Depends(get_current_user)):
    with get_db() as db:
        db.execute(
            "SELECT * FROM bots WHERE id=%s AND user_id=%s", (bot_id, user["id"])
        )
        bot = db.fetchone()
        if not bot:
            raise HTTPException(404, "Бот не найден")
        new_active = 0 if bot["active"] else 1
        db.execute("UPDATE bots SET active=%s WHERE id=%s", (new_active, bot_id))
    return {"active": bool(new_active)}
 
 
@app.post("/api/bots/{bot_id}/set-webhook")
async def set_webhook(bot_id: int, request: Request, user=Depends(get_current_user)):
    with get_db() as db:
        db.execute(
            "SELECT * FROM bots WHERE id=%s AND user_id=%s", (bot_id, user["id"])
        )
        bot = db.fetchone()
    if not bot:
        raise HTTPException(404, "Бот не найден")
    body = await request.json()
    base_url = body.get("base_url", "").rstrip("/")
    if not base_url:
        raise HTTPException(400, "Укажите base_url")
    webhook_url = f"{base_url}/webhook/{bot['token']}"
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"https://api.telegram.org/bot{bot['token']}/setWebhook",
            json={"url": webhook_url, "allowed_updates": ["message", "callback_query"]},
            timeout=10,
        )
    data = r.json()
    if not data.get("ok"):
        raise HTTPException(400, f"Telegram error: {data.get('description')}")
    return {"ok": True, "webhook_url": webhook_url}
 
 
@app.delete("/api/bots/{bot_id}/set-webhook")
async def delete_webhook(bot_id: int, user=Depends(get_current_user)):
    with get_db() as db:
        db.execute(
            "SELECT * FROM bots WHERE id=%s AND user_id=%s", (bot_id, user["id"])
        )
        bot = db.fetchone()
    if not bot:
        raise HTTPException(404, "Бот не найден")
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"https://api.telegram.org/bot{bot['token']}/deleteWebhook", timeout=10
        )
    return {"ok": r.json().get("ok", False)}
 
 
@app.get("/api/bots/{bot_id}/webhook-info")
async def get_webhook_info(bot_id: int, user=Depends(get_current_user)):
    with get_db() as db:
        db.execute(
            "SELECT * FROM bots WHERE id=%s AND user_id=%s", (bot_id, user["id"])
        )
        bot = db.fetchone()
    if not bot:
        raise HTTPException(404, "Бот не найден")
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://api.telegram.org/bot{bot['token']}/getWebhookInfo", timeout=10
        )
    return r.json()
 
 
# ─── Scenario routes ──────────────────────────────────────────────────────────
 
def _serialize_scenario(row: dict) -> dict:
    d = dict(row)
    d["nodes"] = json.loads(d.get("nodes") or "[]")
    d["edges"] = json.loads(d.get("edges") or "[]")
    return d
 
 
@app.get("/api/scenarios")
def get_scenarios(bot_id: Optional[int] = None, user=Depends(get_current_user)):
    with get_db() as db:
        if bot_id:
            db.execute(
                "SELECT * FROM scenarios WHERE user_id=%s AND bot_id=%s ORDER BY updated_at DESC",
                (user["id"], bot_id)
            )
        else:
            db.execute(
                "SELECT * FROM scenarios WHERE user_id=%s ORDER BY updated_at DESC",
                (user["id"],)
            )
        rows = db.fetchall()
    return [_serialize_scenario(r) for r in rows]
 
 
@app.post("/api/scenarios")
def create_scenario(body: ScenarioBody, user=Depends(get_current_user)):
    now = int(time.time())
    with get_db() as db:
        db.execute(
            "SELECT id FROM bots WHERE id=%s AND user_id=%s", (body.bot_id, user["id"])
        )
        bot = db.fetchone()
        if not bot:
            raise HTTPException(404, "Бот не найден")
        db.execute(
            """INSERT INTO scenarios
               (bot_id, user_id, name, description, `trigger`, nodes, edges, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (body.bot_id, user["id"], body.name, body.description,
             body.trigger, json.dumps(body.nodes), json.dumps(body.edges), now, now)
        )
        scenario_id = db.lastrowid
        db.execute("SELECT * FROM scenarios WHERE id=%s", (scenario_id,))
        row = db.fetchone()
    return _serialize_scenario(row)
 
 
@app.get("/api/scenarios/{scenario_id}")
def get_scenario(scenario_id: int, user=Depends(get_current_user)):
    with get_db() as db:
        db.execute(
            "SELECT * FROM scenarios WHERE id=%s AND user_id=%s",
            (scenario_id, user["id"])
        )
        row = db.fetchone()
    if not row:
        raise HTTPException(404, "Сценарий не найден")
    return _serialize_scenario(row)
 
 
@app.patch("/api/scenarios/{scenario_id}")
def update_scenario(scenario_id: int, body: UpdateScenarioBody, user=Depends(get_current_user)):
    now = int(time.time())
    with get_db() as db:
        db.execute(
            "SELECT id FROM scenarios WHERE id=%s AND user_id=%s",
            (scenario_id, user["id"])
        )
        if not db.fetchone():
            raise HTTPException(404, "Сценарий не найден")
 
        fields = ["updated_at=%s"]
        vals   = [now]
        if body.name        is not None: fields.append("name=%s");        vals.append(body.name)
        if body.description is not None: fields.append("description=%s"); vals.append(body.description)
        if body.trigger     is not None: fields.append("`trigger`=%s");     vals.append(body.trigger)
        if body.nodes       is not None: fields.append("nodes=%s");       vals.append(json.dumps(body.nodes))
        if body.edges       is not None: fields.append("edges=%s");       vals.append(json.dumps(body.edges))
        if body.active      is not None: fields.append("active=%s");      vals.append(1 if body.active else 0)
        vals.append(scenario_id)
        db.execute(f"UPDATE scenarios SET {', '.join(fields)} WHERE id=%s", vals)
        db.execute("SELECT * FROM scenarios WHERE id=%s", (scenario_id,))
        row = db.fetchone()
    return _serialize_scenario(row)
 
 
@app.delete("/api/scenarios/{scenario_id}")
def delete_scenario(scenario_id: int, user=Depends(get_current_user)):
    with get_db() as db:
        db.execute(
            "SELECT id FROM scenarios WHERE id=%s AND user_id=%s",
            (scenario_id, user["id"])
        )
        if not db.fetchone():
            raise HTTPException(404, "Сценарий не найден")
        db.execute("DELETE FROM scenarios WHERE id=%s", (scenario_id,))
    return {"ok": True}
 
 
# ─── Webhook ──────────────────────────────────────────────────────────────────
 
@app.post("/webhook/{bot_token}")
async def telegram_webhook(bot_token: str, update: WebhookUpdate):
    with get_db() as db:
        db.execute(
            "SELECT * FROM bots WHERE token=%s AND active=1", (bot_token,)
        )
        bot_row = db.fetchone()
    if not bot_row:
        return {"ok": False}
 
    bot         = dict(bot_row)
    chat_id     = None
    user_text   = ""
    callback_id = None
    is_callback = False
 
    if update.message:
        chat_id   = update.message.get("chat", {}).get("id")
        user_text = (update.message.get("text") or "").strip()
    elif update.callback_query:
        chat_id     = update.callback_query.get("message", {}).get("chat", {}).get("id")
        user_text   = (update.callback_query.get("data") or "").strip()
        callback_id = update.callback_query.get("id")
        is_callback = True
 
    if not chat_id:
        return {"ok": True}
 
    if is_callback and user_text.startswith("goto:"):
        await handle_goto(bot, chat_id, user_text[5:], callback_id)
        return {"ok": True}
 
    if not is_callback:
        resumed = await resume_scenario(bot, chat_id, user_text, callback_id)
        if resumed:
            return {"ok": True}
 
    if not user_text:
        return {"ok": True}
 
    scenario = find_active_scenario(bot["id"], user_text)
    if not scenario:
        return {"ok": True}
 
    await execute_scenario(bot, scenario, chat_id, user_text, callback_id)
    return {"ok": True}
 
 
# ─── Health ───────────────────────────────────────────────────────────────────
 
@app.get("/api/health")
def health():
    return {"status": "ok", "service": "BOTOLABR API v2"}