# مِلك - نظام إدارة الاستثمار العقاري

نظام Django عربي لإدارة المشاريع العقارية المتعددة، الأراضي، المساهمين، المساهمات، المصروفات، المبيعات، العمليات المالية وتوزيع الأرباح.

## التشغيل

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

افتح `http://127.0.0.1:8000/` للوحة المتابعة، أو `http://127.0.0.1:8000/admin/` لإدخال البيانات.

كل مشروع مستقل ويمكن أن يعمل بالتوازي مع مشاريع أخرى. كل مساهمة أو عملية مالية أو مصروف أو بيع يُحفظ كسجل منفصل مع التاريخ والوقت.

الأمر `seed_demo` يضيف بيانات تجريبية بسيطة لعمارتين مستقلتين. يمكن تشغيله أكثر من مرة دون تكرار السجلات التجريبية.

## النشر على الإنترنت

الملف `render.yaml` مجهز للنشر على Render مع PostgreSQL وGunicorn وHTTPS.

1. ارفع المشروع إلى GitHub.
2. في Render اختر **New Blueprint** واربط مستودع GitHub.
3. سيقرأ Render ملف `render.yaml` وينشئ الموقع وقاعدة البيانات.
4. أضف النطاق `mohammedameein-realestate.com` من إعدادات الموقع.
5. في شركة النطاق أضف سجل `CNAME` الذي يعطيه Render للنطاق `www`، وسجل `A` أو إعادة توجيه للنطاق الأساسي حسب تعليمات Render.
6. بعد نجاح الربط افتح `https://mohammedameein-realestate.com`.

بعد أول نشر أنشئ مستخدم الإدارة من Shell الخاص بالخدمة:

```bash
python manage.py createsuperuser
```

لا تضع `DJANGO_SECRET_KEY` أو كلمة مرور قاعدة البيانات داخل GitHub؛ ملف `render.yaml` ينشئ المفتاح السري تلقائيًا.
