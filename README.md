# TigerOps — النسخة الأولى (تحويل بنكي + واتساب)

منصة بسيطة لاشتراكات شهرية، بدون تعقيد، مناسبة لواقع الدفع في السودان.

## شنو جوه المشروع؟
- `app.py` — السيرفر (Flask).
- `config.py` — عدّل هنا: اسم مشروعك، السعر، رقم واتساب، بيانات بنكك.
- `database.py` — تخزين الاشتراكات (SQLite).
- `templates/` — صفحات الموقع.
- `static/css/style.css` — التصميم.

## قبل أي شي: عدّل ملف config.py
افتحو وغيّر:
- `WHATSAPP_NUMBER`
- `BANKAK_ACCOUNT_NAME`
- `BANKAK_ACCOUNT_NUMBER`
- `SUBSCRIPTION_PRICE_USD` (لو حبيت تغيّر السعر)

## كيف تشتغل العملية؟
1. العميل يفتح `/subscribe`، يشوف السعر وبيانات بنكك.
2. يحوّل، وبعدين يعبي اسمه ورقمه في الفورم.
3. أنت تدخل لوحة التحكم السرية على:
   `/tiger-admin-7421`
   (غيّر هذا الاسم في app.py لشي يخصك بس، عشان ما يلقاه أي زول بالصدفة)
4. تشوف الطلبات المعلّقة، وتضغط "تفعيل" بعد ما تتأكد من الإيصال.

## رفع المشروع على GitHub (من الموبايل، بدون أوامر معقدة)
1. روح لـ github.com وسجّل دخول.
2. اضغط "+" فوق → "New repository".
3. اكتب اسم (مثلاً `tiger-saas`) → اضغط "Create repository".
4. في صفحة المستودع الجديد، اضغط "uploading an existing file".
5. اختار كل الملفات والمجلدات من جهازك (templates, static, app.py, إلخ) واسحبها/ارفعها.
6. اكتب رسالة بسيطة في "Commit changes" واضغط "Commit changes".

⚠️ **مهم:** ما ترفع ملف `.env` لو سويتو فيما بعد — فيه أسرارك.

## النشر على Render
1. سجل في render.com → "New" → "Web Service".
2. اربط حساب GitHub واختار المستودع.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. أضف Environment Variable: `SECRET_KEY` بقيمة عشوائية طويلة.
6. اضغط Deploy.

## الخطوة الجاية (بعد ما الأساس ده يشتغل)
- إضافة Crypto Pay كخيار دفع إضافي.
- لوحة تحكم AI (ساعات الشغل + التحويل لإنسان عند الخطأ).
- ربط Gemini API للردود الذكية.
