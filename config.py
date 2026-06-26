"""
إعدادات المشروع - عدّل القيم هنا حسب مشروعك.
"""
import os

# اسم منصتك (غيّرو لاسم مشروعك الحقيقي)
PLATFORM_NAME = "TigerOps"

# سعر الاشتراك الشهري بالدولار
SUBSCRIPTION_PRICE_USD = "5"

# رقم واتساب لاستقبال إيصالات الدفع والدعم (بصيغة دولية بدون + أو 00)
# مثال: لو رقمك 0912345678 يكتب 249912345678
WHATSAPP_NUMBER = "249XXXXXXXXX"

# بيانات حساب بنكك / ماي كاشي لاستقبال التحويلات
BANKAK_ACCOUNT_NAME = "اسمك هنا"
BANKAK_ACCOUNT_NUMBER = "رقم حسابك هنا"

# مفتاح Flask السري (اقرأه من متغير بيئة، وفي التطوير المحلي يستخدم قيمة افتراضية)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
