"""
طبقة قاعدة البيانات - SQLite بسيطة لتخزين الاشتراكات.
كافية للبداية؛ لو كبر المشروع بعدين ممكن تنقل لـ PostgreSQL.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "subscriptions.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            invoice_id TEXT UNIQUE NOT NULL,
            amount TEXT NOT NULL,
            asset TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            expires_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def create_pending_subscription(customer_name, contact, invoice_id, amount, asset):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO subscriptions (customer_name, contact, invoice_id, amount, asset, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'pending', ?)
        """,
        (customer_name, contact, invoice_id, amount, asset, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()


def activate_subscription(invoice_id, expires_at):
    conn = get_connection()
    conn.execute(
        """
        UPDATE subscriptions
        SET status = 'active', expires_at = ?
        WHERE invoice_id = ?
        """,
        (expires_at, invoice_id),
    )
    conn.commit()
    conn.close()


def get_subscription_by_invoice(invoice_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM subscriptions WHERE invoice_id = ?", (invoice_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_active_subscriptions():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM subscriptions WHERE status = 'active' ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_pending_subscriptions():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM subscriptions WHERE status = 'pending' ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def activate_subscription_by_id(sub_id, expires_at):
    conn = get_connection()
    conn.execute(
        "UPDATE subscriptions SET status = 'active', expires_at = ? WHERE id = ?",
        (expires_at, sub_id),
    )
    conn.commit()
    conn.close()
