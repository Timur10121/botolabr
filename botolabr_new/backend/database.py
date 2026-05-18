"""
BOTOLABR — Database layer (MySQL)
Использует PyMySQL + connection pool через DBUtils.
"""

import json
import time
import os
from contextlib import contextmanager

import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB

# ── Конфигурация из переменных окружения ──────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     int(os.getenv("DB_PORT", "3306")),
    "user":     os.getenv("DB_USER",     "botolabr"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME",     "botolabr"),
    "charset":  "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": False,
}

# ── Connection pool ────────────────────────────────────────────────────────
_pool: PooledDB | None = None

def get_pool() -> PooledDB:
    global _pool
    if _pool is None:
        cfg = {k: v for k, v in DB_CONFIG.items() if k != "cursorclass"}
        _pool = PooledDB(
            creator=pymysql,
            maxconnections=20,
            mincached=2,
            maxcached=10,
            blocking=True,
            ping=1,
            **cfg,
            cursorclass=pymysql.cursors.DictCursor,
        )
    return _pool


@contextmanager
def get_db():
    pool = get_pool()
    conn = pool.connection()
    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Создание таблиц ────────────────────────────────────────────────────────

def init_db():
    """Создаёт все таблицы если их нет. Безопасно запускать при каждом старте."""

    statements = [
        "SET SESSION sql_mode = ''",

        """
        CREATE TABLE IF NOT EXISTS users (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            username   VARCHAR(64)  UNIQUE NOT NULL,
            email      VARCHAR(255) UNIQUE NOT NULL,
            password   VARCHAR(255) NOT NULL,
            name       VARCHAR(128) DEFAULT '',
            lastname   VARCHAR(128) DEFAULT '',
            avatar     LONGTEXT     DEFAULT NULL,
            created_at INT          DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,

        """
        CREATE TABLE IF NOT EXISTS sessions (
            token      VARCHAR(64) PRIMARY KEY,
            user_id    INT         NOT NULL,
            expires_at INT         NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        """
        CREATE TABLE IF NOT EXISTS bots (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            user_id      INT          NOT NULL,
            token        VARCHAR(128) NOT NULL,
            bot_username VARCHAR(128) NOT NULL,
            bot_name     VARCHAR(255) NOT NULL,
            active       TINYINT(1)   DEFAULT 1,
            connected_at INT          DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,

        """
        CREATE TABLE IF NOT EXISTS scenarios (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            bot_id      INT          NOT NULL,
            user_id     INT          NOT NULL,
            name        VARCHAR(255) NOT NULL,
            description TEXT         DEFAULT NULL,
            `trigger`   VARCHAR(255) DEFAULT '',
            nodes       LONGTEXT     NULL,
            edges       LONGTEXT     NULL,
            active      TINYINT(1)   DEFAULT 0,
            created_at  INT          DEFAULT 0,
            updated_at  INT          DEFAULT 0,
            FOREIGN KEY (bot_id)  REFERENCES bots(id)  ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,

        """
        CREATE TABLE IF NOT EXISTS user_states (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            bot_id       INT          NOT NULL,
            chat_id      BIGINT       NOT NULL,
            scenario_id  INT          NOT NULL,
            current_node VARCHAR(64)  NOT NULL,
            data         LONGTEXT     NULL,
            updated_at   INT          DEFAULT 0,
            UNIQUE KEY uq_bot_chat (bot_id, chat_id),
            FOREIGN KEY (bot_id)      REFERENCES bots(id)      ON DELETE CASCADE,
            FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
    ]

    for stmt in statements:
        with get_db() as db:
            db.execute(stmt)

    print("[DB] Таблицы инициализированы.")


# ── User state helpers ─────────────────────────────────────────────────────

def get_user_state(bot_id: int, chat_id: int) -> dict | None:
    with get_db() as db:
        db.execute(
            "SELECT * FROM user_states WHERE bot_id=%s AND chat_id=%s",
            (bot_id, chat_id)
        )
        row = db.fetchone()
    if not row:
        return None
    row["data"] = json.loads(row.get("data") or "{}")
    return row


def save_user_state(bot_id: int, chat_id: int, scenario_id: int, current_node: str, data: dict = None):
    data_str = json.dumps(data or {})
    now = int(time.time())
    with get_db() as db:
        db.execute(
            """
            INSERT INTO user_states (bot_id, chat_id, scenario_id, current_node, data, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                scenario_id  = VALUES(scenario_id),
                current_node = VALUES(current_node),
                data         = VALUES(data),
                updated_at   = VALUES(updated_at)
            """,
            (bot_id, chat_id, scenario_id, current_node, data_str, now)
        )


def clear_user_state(bot_id: int, chat_id: int):
    with get_db() as db:
        db.execute(
            "DELETE FROM user_states WHERE bot_id=%s AND chat_id=%s",
            (bot_id, chat_id)
        )