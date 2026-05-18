"""
polling.py — Long polling для BOTOLABR
Запуск: py polling.py
Не нужен webhook — бот сам опрашивает Telegram.
"""

import asyncio
import httpx
from database import get_db
from scenario_engine import (
    find_active_scenario,
    execute_scenario,
    resume_scenario,
    handle_goto,
)

POLL_INTERVAL = 1  # секунд между циклами когда нет обновлений


async def get_updates(token: str, offset: int = 0) -> list:
    """Long polling: ждём обновления до 30 сек."""
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.telegram.org/bot{token}/getUpdates",
                params={
                    "offset":          offset,
                    "timeout":         30,
                    "allowed_updates": ["message", "callback_query"],
                },
                timeout=35,
            )
        data = r.json()
        if data.get("ok"):
            return data["result"]
    except Exception as e:
        print(f"[polling] Ошибка getUpdates: {e}")
    return []


async def process_update(bot: dict, update: dict):
    """Обработать одно обновление от Telegram."""

    # ── Текстовое сообщение ───────────────────────────────────────────────
    if "message" in update:
        msg     = update["message"]
        chat_id = msg["chat"]["id"]
        text    = msg.get("text", "")

        if not text:
            return

        # 1. Продолжаем сценарий если пользователь в состоянии ожидания
        if await resume_scenario(bot, chat_id, text):
            return

        # 2. Ищем сценарий по триггеру
        scenario = find_active_scenario(bot["id"], text)
        if scenario:
            await execute_scenario(bot, scenario, chat_id, text)

    # ── Нажатие inline-кнопки ─────────────────────────────────────────────
    elif "callback_query" in update:
        cq          = update["callback_query"]
        chat_id     = cq["message"]["chat"]["id"]
        cb_data     = cq.get("data", "")
        callback_id = cq["id"]

        if cb_data.startswith("goto:"):
            target_node_id = cb_data[len("goto:"):]
            await handle_goto(bot, chat_id, target_node_id, callback_id)
        else:
            # Передаём как текст — resume подхватит если ждём ввод
            await resume_scenario(bot, chat_id, cb_data, callback_id)


def load_active_bots() -> list:
    """Загружает всех активных ботов из БД."""
    try:
        with get_db() as db:
            rows = db.execute("SELECT * FROM bots WHERE active=1").fetchall()
            return [dict(r) for r in rows]
    except Exception as e:
        print(f"[polling] Ошибка чтения ботов: {e}")
        return []


async def poll_bot(bot: dict, offsets: dict):
    """Один цикл polling для одного бота."""
    bot_id = bot["id"]
    offset = offsets.get(bot_id, 0)

    updates = await get_updates(bot["token"], offset)

    for upd in updates:
        try:
            await process_update(bot, upd)
        except Exception as e:
            print(f"[bot {bot_id}] Ошибка обработки update: {e}")
        offset = upd["update_id"] + 1

    if updates:
        offsets[bot_id] = offset


async def main():
    print("=" * 40)
    print("  BOTOLABR Polling запущен")
    print("  Ctrl+C для остановки")
    print("=" * 40)

    offsets = {}

    while True:
        bots = load_active_bots()

        if not bots:
            print("[polling] Нет активных ботов, ожидание...")
            await asyncio.sleep(5)
            continue

        # Опрашиваем всех ботов параллельно
        await asyncio.gather(
            *[poll_bot(bot, offsets) for bot in bots],
            return_exceptions=True,
        )

        await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[polling] Остановлен.")