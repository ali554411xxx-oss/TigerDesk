"""
app.py - النسخة الأولى المبسطة من المنصة.
الفكرة: العميل يشاهد السعر، يحول عبر بنكك/ماي كاشي، يبعت إيصال الدفع
عبر واتساب، وأنت تفعّل اشتراكه يدوياً من خلال رابط بسيط.

لاحقاً (خطوة جاية): نضيف Crypto Pay كخيار إضافي، ولوحة تحكم AI.
"""
import os
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, request, redirect, url_for, abort

import config
import database

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

database.init_db()


@app.route("/")
def index():
    return render_template(
        "index.html",
        platform_name=config.PLATFORM_NAME,
        price=config.SUBSCRIPTION_PRICE_USD,
    )


@app.route("/subscribe", methods=["GET"])
def subscribe():
    whatsapp_link = f"https://wa.me/{config.WHATSAPP_NUMBER}"
    return render_template(
        "subscribe.html",
        platform_name=config.PLATFORM_NAME,
        price=config.SUBSCRIPTION_PRICE_USD,
        bankak_name=config.BANKAK_ACCOUNT_NAME,
        bankak_number=config.BANKAK_ACCOUNT_NUMBER,
        whatsapp_link=whatsapp_link,
    )


@app.route("/request-activation", methods=["POST"])
def request_activation():
    """
    العميل يعبي اسمه ووسيلة تواصله بعد ما يحول، عشان يدخل في
    قائمة الانتظار وأنت تفعّله يدوياً بعد التأكد من الإيصال.
    """
    customer_name = request.form.get("name", "").strip()
    contact = request.form.get("contact", "").strip()

    if not customer_name or not contact:
        return redirect(url_for("subscribe"))

    database.create_pending_subscription(
        customer_name=customer_name,
        contact=contact,
        invoice_id=f"manual-{int(datetime.now(timezone.utc).timestamp())}",
        amount=config.SUBSCRIPTION_PRICE_USD,
        asset="bankak",
    )

    return render_template(
        "thanks.html",
        platform_name=config.PLATFORM_NAME,
        whatsapp_link=f"https://wa.me/{config.WHATSAPP_NUMBER}",
    )


# ---------------------------------------------------------------------------
# لوحة تحكم مبسطة عشانك بس (تفعيل الاشتراكات المعلّقة يدوياً)
# لاحقاً نحميها بكلمة سر حقيقية، حالياً نخليها مخفية بمسار سري بس
# ---------------------------------------------------------------------------
ADMIN_SECRET_PATH = "tiger-admin-7421"  # غيّر الرقم/الكلمة دي لشي يخصك بس


@app.route(f"/{ADMIN_SECRET_PATH}")
def admin_panel():
    pending = database.get_pending_subscriptions()
    active = database.get_active_subscriptions()
    return render_template("admin.html", pending=pending, active=active)


@app.route(f"/{ADMIN_SECRET_PATH}/activate/<int:sub_id>", methods=["POST"])
def activate(sub_id):
    expires_at = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    database.activate_subscription_by_id(sub_id, expires_at)
    return redirect(url_for("admin_panel"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
