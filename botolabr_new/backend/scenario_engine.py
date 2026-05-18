"""
BOTOLABR — Scenario Engine
Выполняет сценарий по node-based структуре с поддержкой состояний пользователя.
"""

import asyncio
import json
import httpx
from typing import Optional

from database import get_db, get_user_state, save_user_state, clear_user_state


# ── Telegram helpers ───────────────────────────────────────────────────────

async def send_tg_message(token: str, chat_id: int, text: str, reply_markup=None):
    payload = {
        "chat_id":    chat_id,
        "text":       text or "…",
        "parse_mode": "Markdown",
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json=payload,
            timeout=10,
        )


async def send_tg_photo(token: str, chat_id: int, url: str, caption: str = ""):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{token}/sendPhoto",
            json={"chat_id": chat_id, "photo": url, "caption": caption},
            timeout=10,
        )


async def answer_callback(token: str, callback_id: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{token}/answerCallbackQuery",
            json={"callback_query_id": callback_id},
            timeout=5,
        )


# ── Scenario loader ────────────────────────────────────────────────────────

def find_active_scenario(bot_id: int, trigger: str) -> Optional[dict]:
    """Ищет активный сценарий у бота, чей trigger совпадает с командой."""
    with get_db() as db:
        db.execute(
            "SELECT * FROM scenarios WHERE bot_id=%s AND active=1 ORDER BY id ASC",
            (bot_id,),
        )
        rows = db.fetchall()

    trigger_clean = trigger.strip().lower()

    for row in rows:
        d = dict(row)
        d["nodes"] = json.loads(d.get("nodes") or "[]")
        d["edges"] = json.loads(d.get("edges") or "[]")
        scen_trigger = (d.get("trigger") or "").strip().lower()
        if scen_trigger and scen_trigger == trigger_clean:
            return d

    if trigger_clean == "/start":
        for row in rows:
            d = dict(row)
            d["nodes"] = json.loads(d.get("nodes") or "[]")
            d["edges"] = json.loads(d.get("edges") or "[]")
            if not (d.get("trigger") or "").strip():
                return d
        if rows:
            d = dict(rows[0])
            d["nodes"] = json.loads(d.get("nodes") or "[]")
            d["edges"] = json.loads(d.get("edges") or "[]")
            return d

    return None


def get_scenario_by_id(scenario_id: int) -> Optional[dict]:
    with get_db() as db:
        db.execute("SELECT * FROM scenarios WHERE id=%s", (scenario_id,))
        row = db.fetchone()
    if not row:
        return None
    d = dict(row)
    d["nodes"] = json.loads(d.get("nodes") or "[]")
    d["edges"] = json.loads(d.get("edges") or "[]")
    return d


# ── Node helpers ───────────────────────────────────────────────────────────

def find_node(nodes: list, node_id: str) -> Optional[dict]:
    for n in nodes:
        if n.get("id") == node_id:
            return n
    return None


def find_start_node(nodes: list) -> Optional[dict]:
    for n in nodes:
        if n.get("type") == "start":
            return n
    return nodes[0] if nodes else None


def next_node_by_edge(nodes: list, edges: list, current_id: str, edge_label: str = None) -> Optional[dict]:
    candidates = [e for e in edges if e.get("source") == current_id]
    if not candidates:
        return None
    if edge_label:
        for e in candidates:
            if (e.get("label") or "").strip().lower() == edge_label.strip().lower():
                return find_node(nodes, e["target"])
    return find_node(nodes, candidates[0]["target"])


# ── Main executor ──────────────────────────────────────────────────────────

async def execute_scenario(bot: dict, scenario: dict, chat_id: int, user_text: str, callback_id: str = None):
    nodes  = scenario.get("nodes", [])
    edges  = scenario.get("edges", [])
    token  = bot["token"]
    bot_id = bot["id"]

    if not nodes:
        return

    start = find_start_node(nodes)
    if not start:
        return

    current = next_node_by_edge(nodes, edges, start["id"]) or start
    await _walk(token, bot_id, chat_id, scenario["id"], nodes, edges, current, user_text, callback_id)


async def resume_scenario(bot: dict, chat_id: int, user_text: str, callback_id: str = None):
    state = get_user_state(bot["id"], chat_id)
    if not state:
        return False

    scenario = get_scenario_by_id(state["scenario_id"])
    if not scenario:
        clear_user_state(bot["id"], chat_id)
        return False

    nodes  = scenario["nodes"]
    edges  = scenario["edges"]
    bot_id = bot["id"]

    current_node = find_node(nodes, state["current_node"])
    if not current_node:
        clear_user_state(bot["id"], chat_id)
        return False

    saved_data = state.get("data", {})
    field_name = (current_node.get("data") or {}).get("variable") or f"input_{state['current_node']}"
    saved_data[field_name] = user_text

    nxt = next_node_by_edge(nodes, edges, state["current_node"])
    if not nxt:
        clear_user_state(bot["id"], chat_id)
        return True

    await _walk(bot["token"], bot_id, chat_id, state["scenario_id"], nodes, edges, nxt, user_text, callback_id, saved_data)
    return True


async def handle_goto(bot: dict, chat_id: int, target_node_id: str, callback_id: str = None):
    state = get_user_state(bot["id"], chat_id)
    scenario_id = state["scenario_id"] if state else None

    if not scenario_id:
        with get_db() as db:
            db.execute(
                "SELECT * FROM scenarios WHERE bot_id=%s AND active=1",
                (bot["id"],)
            )
            rows = db.fetchall()
        for row in rows:
            d = dict(row)
            d["nodes"] = json.loads(d.get("nodes") or "[]")
            d["edges"] = json.loads(d.get("edges") or "[]")
            if find_node(d["nodes"], target_node_id):
                scenario_id = d["id"]
                break

    if not scenario_id:
        return False

    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        return False

    nodes  = scenario["nodes"]
    edges  = scenario["edges"]
    target = find_node(nodes, target_node_id)
    if not target:
        return False

    if callback_id:
        await answer_callback(bot["token"], callback_id)

    saved_data = state.get("data", {}) if state else {}
    await _walk(bot["token"], bot["id"], chat_id, scenario_id, nodes, edges, target, "", callback_id, saved_data)
    return True


# ── Walker ─────────────────────────────────────────────────────────────────

async def _walk(token, bot_id, chat_id, scenario_id, nodes, edges, current, user_text, callback_id, data=None):
    data    = data or {}
    visited = set()

    while current:
        node_id   = current.get("id")
        node_type = current.get("type", "message")
        node_data = current.get("data") or {}

        if node_id in visited:
            break
        visited.add(node_id)

        if node_type == "message":
            text = node_data.get("text", "")
            await send_tg_message(token, chat_id, text)

        elif node_type == "buttons":
            text    = node_data.get("text", "Выберите:")
            buttons = node_data.get("buttons", [])
            keyboard = []
            for btn in buttons:
                btn_text = btn.get("text", "")
                btn_next = btn.get("next", "")
                cb_data  = f"goto:{btn_next}" if btn_next else btn_text
                keyboard.append([{"text": btn_text, "callback_data": cb_data}])
            markup = {"inline_keyboard": keyboard} if keyboard else None
            await send_tg_message(token, chat_id, text, markup)
            save_user_state(bot_id, chat_id, scenario_id, node_id, data)
            return

        elif node_type == "image":
            url     = node_data.get("url", "")
            caption = node_data.get("caption", "")
            if url:
                await send_tg_photo(token, chat_id, url, caption)

        elif node_type == "delay":
            secs = min(int(node_data.get("seconds", 2)), 10)
            await asyncio.sleep(secs)

        elif node_type == "input":
            prompt = node_data.get("text", "Введите ответ:")
            await send_tg_message(token, chat_id, prompt)
            save_user_state(bot_id, chat_id, scenario_id, node_id, data)
            return

        elif node_type == "condition":
            variable = node_data.get("variable", "")
            operator = node_data.get("operator", "==")
            value    = node_data.get("value", "")
            actual   = str(data.get(variable, ""))
            matched  = False
            if operator == "==":       matched = actual == str(value)
            elif operator == "!=":     matched = actual != str(value)
            elif operator == "contains": matched = str(value) in actual
            label = "true" if matched else "false"
            nxt = next_node_by_edge(nodes, edges, node_id, label)
            if nxt:
                current = nxt
                continue
            break

        elif node_type == "goto":
            target_id = node_data.get("target", "")
            target    = find_node(nodes, target_id)
            if target:
                current = target
                continue
            break

        elif node_type in ("end", "start"):
            if node_type == "end":
                clear_user_state(bot_id, chat_id)

        nxt = next_node_by_edge(nodes, edges, node_id)
        current = nxt