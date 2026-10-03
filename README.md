# ☀️ تقویم شمسی ایران برای Apple Calendar

تقویم قابل اشتراک برای iPhone / Apple Calendar با **تاریخ شمسی + مناسبت‌ها + تعطیلات**.

## امکانات
- رویدادهای تمام روز (All-day)
- تاریخ شمسی داخل عنوان هر رویداد، مثل `☀️ 1405/07/07`
- چند مناسبت یک روز در یک رویداد
- مشخص‌شدن تعطیلات با دسته‌بندی
- لینک داخل هر Event برای مشاهده/جست‌وجوی توضیحات رخداد
- تولید خودکار فایل `calendar.ics` با GitHub Actions
- بدون سرور یا هاست پولی؛ مناسب GitHub Pages

## راه‌اندازی روی GitHub

1. یک Repository جدید بساز، مثلاً `iran-shamsi-apple-calendar`.
2. همه فایل‌های این پروژه را داخل Repository آپلود کن.
3. از Settings → Pages، بخش **Build and deployment** را روی **Deploy from a branch** بگذار.
4. Branch را روی `main` و Folder را روی `/ (root)` قرار بده.
5. چند لحظه بعد GitHub Pages یک آدرس شبیه این می‌دهد:

```text
https://USERNAME.github.io/iran-shamsi-apple-calendar/
```

فایل تقویم:

```text
https://USERNAME.github.io/iran-shamsi-apple-calendar/calendar.ics
```

## افزودن به iPhone

در iPhone به:

**Settings → Apps → Calendar → Calendar Accounts → Add Account → Other → Add Subscribed Calendar**

برو و URL فایل `calendar.ics` را وارد کن.

یا لینک فایل را در Safari باز کن و گزینه افزودن تقویم را دنبال کن.

## نحوه به‌روزرسانی

GitHub Actions هنگام Push و به‌صورت ماهانه `calendar.ics` را دوباره تولید می‌کند. بنابراین لینک اشتراک ثابت می‌ماند و فایل تقویم به‌روزرسانی می‌شود.

## منبع داده

داده‌های پایه از پروژه عمومی `alirezadesh/jalali_calendar` گرفته می‌شوند که داده روزانه، تاریخ میلادی معادل، تعطیلات و رویدادهای سال‌های مختلف را ارائه می‌کند.

## نکته درباره لینک رویداد

Apple Calendar لینک `URL` هر Event را نمایش می‌دهد. برای اینکه برای همه مناسبت‌ها یک مقصد دقیق قابل‌اعتماد وجود داشته باشد، پروژه به‌صورت پیش‌فرض لینک جست‌وجوی عنوان رخداد در ویکی‌پدیای فارسی را قرار می‌دهد. این لینک را می‌توان بعداً به دیتابیس لینک‌های دقیق‌تر تبدیل کرد.
