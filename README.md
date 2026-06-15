# سیستم مدیریت و انتشار خودکار محتوای اینستاگرام از طریق ربات تلگرام
# Instagram Automation System via Telegram Bot

---

## بخش اول: مستندات فارسی (Persian Documentation)

این پروژه یک سیستم اتوماسیون چندکاربره برای مدیریت، زمان‌بندی و انتشار خودکار محتوا (عکس و ویدیو) در صفحات اینستاگرام است که از طریق یک ربات تلگرام به عنوان پنل مدیریتی کنترل می‌شود. با استفاده از این سیستم، مدیران می‌توانند بدون نیاز به ورود مستقیم به صفحات اینستاگرام، محتوای خود را از طریق تلگرام آپلود کرده و زمان‌بندی انتشار متوازن آن‌ها را به ربات بسپارند.

---

### ویژگی‌های کلیدی سیستم
*   **مدیریت همزمان چند اکانت:** امکان اضافه، حذف و پیکربندی مجدد پیج‌های اینستاگرام از طریق ربات تلگرام.
*   **پشتیبانی از تایید دو مرحله‌ای (2FA):** لاگین کاملاً خودکار به اینستاگرام با استفاده از توکن‌های پویای تولید شده توسط `pyotp`.
*   **زمان‌بندی متوازن خودکار:** سیستم بر اساس تعداد پست درخواستی برای هر پیج در روز، ساعت‌های انتشار را به طور متوازن در طول روز توزیع و زمان‌بندی می‌کند.
*   **پردازش تصاویر و ویدیوها:**
    *   اعمال واترمارک و آیدی صفحه به صورت خودکار روی ویدیوها با فونت دلخواه.
    *   تولید کاور و پیش‌نمایش (Thumbnail) اختصاصی با پس‌زمینه نیمه‌شفاف برای ویدیوها.
    *   پشتیبانی کامل از راست‌چین‌سازی متون فارسی و اصلاح چسبندگی حروف (RTL/Arabic Reshaper).
*   **پیشگیری از جریمه و بلاک اکانت (Anti-Bot):** استفاده از نشست‌های ماندگار (Sessions) برای جلوگیری از لاگین‌های مکرر و بهره‌گیری از سیستم تاخیرهای تصادفی (Random Delays).
*   **کنترل دسترسی:** دسترسی به ربات تلگرام صرفاً برای شناسه‌های عددی (User IDs) تعریف‌شده مجاز است.
*   **سیستم گزارش‌گیری:** ارائه آمار لحظه‌ای از فایل‌های آماده در صف انتظار و تعداد پست‌های ارسال‌شده روزانه.

---

### ساختار پوشه‌ها و فایل‌های پروژه

```text
├── instabot/
│   ├── configs/                             # فایل‌های تنظیمات و گزارش‌های روزانه (JSON)
│   ├── fonts/                               # فونت‌های واژیر و لاله‌زار برای رندر متون روی مدیا
│   │   ├── vazir.ttf                        # فونت متن ویدیوها
│   │   └── lalezar.ttf                      # فونت متن کاورها
│   ├── sessions/                            # نشست‌های اینستاگرام فعال شده جهت دور زدن لاگین مجدد
│   ├── constants.py                         # ثابت‌های بخش اینستاگرام (آدرس‌ها، ابعاد مجاز، CTA)
│   ├── except_exit_func.py                  # توابع مدیریت خروج اضطراری فرآیند
│   ├── instabot.py                          # اسکریپت زمان‌بند اصلی (Scheduler Core)
│   ├── post_uploader.py                     # هسته اعتبارسنجی ابعاد و آپلود محتوا به اینستاگرام
│   ├── read_write_file.py                   # ناظر همگام برای مدیریت دیتابیس JSON تنظیمات پیج‌ها
│   ├── text_on_cover.py                     # رندر متون و تولید کاور سفارشی عکس دار
│   └── text_on_video.py                     # رندر متون و اعمال واترمارک روی فریم‌های ویدیو
│
└── telebot/
    ├── constants.py                         # تنظیمات و توکن ربات تلگرام و شناسه‌های ادمین مجاز
    ├── except_exit_func.py                  # توابع مدیریت خروج اضطراری ربات تلگرام
    ├── insta_login_checker.py               # اعتبار سنجی زنده اطلاعات ورود اینستاگرام
    ├── insta_menus.py                       # منوهای تعاملی، سیستم آپلود محتوا و مدیریت تنظیمات پیج
    ├── read_write_file.py                   # ناظر ناهمگام (Async) برای مدیریت دیتابیس تنظیمات در تلگرام
    ├── show_button.py                       # مدیریت نمایش کیبوردهای شکیل ربات تلگرام
    ├── telebot.py                           # اسکریپت راه‌انداز اصلی ربات تلگرام (Telegram Entry Point)
    └── test.py                              # ابزار پاک کردن سشن اکانت تست
```

---

### پیش‌نیازهای سیستم

1.  **پایتون:** نسخه 3.10 یا بالاتر.
2.  **پکیج‌های سیستم‌عاملی:** برای ویرایش ویدیو با کتابخانه `moviepy` نیاز است ابزار **FFmpeg** بر روی سرور یا سیستم شما نصب و در متغیرهای محیطی سیستم (PATH) قرار گرفته باشد.
3.  **پکیج‌های پایتون:**
    ```bash
    pip install instagrapi python-telegram-bot moviepy pillow pyotp pytz arabic-reshaper python-bidi schedule
    ```

---

### نحوه راه‌اندازی و استفاده

#### گام ۱: پیکربندی متغیرهای امنیتی تلگرام
فایل `telebot/constants.py` را باز کرده و توکن ربات تلگرامی که از `@BotFather` دریافت کرده‌اید را به همراه شناسه عددی اکانت تلگرام خودتان (و سایر مدیران مجاز) وارد کنید:

```python
# telebot/constants.py

# توکن ربات تلگرام شما
my_token = 'YOUR_TELEGRAM_BOT_TOKEN'

# شناسه‌های عددی مجاز برای کنترل ربات
my_user_ids = [
    YOUR_TELEGRAM_USER_ID_1,
    YOUR_TELEGRAM_USER_ID_2
]
```

#### گام ۲: اجرای ربات تلگرام (پنل مدیریت)
برای فعال شدن ربات تلگرام و مدیریت صفحات، دستور زیر را اجرا کنید:
```bash
python telebot/telebot.py
```
سپس در تلگرام دستور `/start` را به ربات ارسال کنید تا منوی مدیریت برای شما باز شود. 

#### گام ۳: اضافه کردن پیج اینستاگرام در تلگرام
1. در منوی ربات، گزینه **Account** و سپس **Add Account** را بزنید.
2. نام کاربری (Username) اینستاگرام را وارد کنید.
3. کلمه عبور (Password) را بفرستید.
4. کلید امنیتی تایید دو مرحله‌ای (**2FA Secret**) را ارسال کنید. (این کلید برای تولید خودکار کدهای موقت زمان ورود به اینستاگرام الزامی است).
5. ربات اطلاعات را به صورت زنده بررسی کرده و در صورت صحت، پوشه و سشن اختصاصی پیج را می‌سازد.

#### گام ۴: ارسال محتوا و تعیین تنظیمات پیج
*   **ارسال پست جدید:** از گزینه **Content** پیج مقصد را انتخاب کرده و عکس یا ویدیو مورد نظرتان را به همراه کپشن در تلگرام برای ربات ارسال کنید. فایل در صف انتظار قرار می‌گیرد.
*   **تعیین تعداد پست در روز:** از گزینه **Setting** پیج خود را انتخاب کرده و مشخص کنید در شبانه‌روز چند پست مایلید منتشر شود (بین ۰ تا ۱۳ پست).
*   **تنظیم کپشن ثابت:** هشتگ‌ها و متن‌های ثابتی که مایلید به انتهای تمام کپشن‌های آن اکانت اضافه شود را وارد کنید.

#### گام ۵: اجرای فرآیند انتشار خودکار (Instabot)
برای اینکه فرآیند زمان‌بندی و انتشار در زمان‌های مشخص به صورت خودکار فعال شود، این اسکریپت را به صورت دائمی (مثلاً با PM2 یا Background Process) روی سرور روشن بگذارید:
```bash
python instabot/instabot.py
```

---

## Part 2: English Documentation

This project is a multi-account Instagram automation system designed to handle the queuing, formatting, scheduling, and automatic publishing of media (images and video clips) across multiple profiles. It is controlled via a secure Telegram bot acting as an administrative panel, allowing admins to upload media and configure pages without logging directly into Instagram.

---

### Key Features
*   **Multi-Account Management:** Add, delete, and configure several Instagram business/creator profiles via Telegram.
*   **2FA Integration:** Supports automatic login using PyOTP to generate dynamic 2-Factor Authentication tokens.
*   **Smart Auto-Scheduling:** Spaces out posts evenly throughout the day depending on your desired daily frequency (0 to 13 posts/day).
*   **Media Processing:**
    *   Applies username watermarks and customizable CALL TO ACTION templates directly onto video frames.
    *   Generates customized preview cover images (thumbnails) with text rendered over a semi-transparent background box.
    *   Fully supports Right-to-Left (RTL) rendering for Persian/Arabic fonts using Arabic reshaper and bidirectional engines.
*   **Anti-Bot & Rate-Limit Protections:** Uses session persistence to limit active login attempts and applies random delay thresholds.
*   **Access Control:** Access to the control panel is strictly limited to authorized Telegram user IDs.
*   **Report Logs:** Shows real-time statistics of local pending items and daily success counts.

---

### Repository Structure

```text
├── instabot/
│   ├── configs/                             # JSON system config databases and success logs
│   ├── fonts/                               # Font files for overlaying text on media assets
│   │   ├── vazir.ttf                        # Font used on video frames
│   │   └── lalezar.ttf                      # Font used on cover images
│   ├── sessions/                            # Saved Instagram authentication states (JSON)
│   ├── constants.py                         # Instabot constants (paths, boundaries, CTA texts)
│   ├── except_exit_func.py                  # Core process crash handlers
│   ├── instabot.py                          # Core timing logic (Scheduler Core)
│   ├── post_uploader.py                     # Media validator and Instagram uploader module
│   ├── read_write_file.py                   # Synchronous configuration database reader/writer
│   ├── text_on_cover.py                     # Text overlay logic for cover thumbnail images
│   └── text_on_video.py                     # Watermark overlay logic for video frames
│
└── telebot/
    ├── constants.py                         # Telegram Bot Token, configuration parameters, and Admin IDs
    ├── except_exit_func.py                  # Telebot process crash handlers
    ├── insta_login_checker.py               # Live validation system for Instagram credentials
    ├── insta_menus.py                       # Interactive Telegram menus, uploading queue handlers, and settings
    ├── read_write_file.py                   # Asynchronous configuration database reader/writer
    ├── show_button.py                       # Helper utility for custom keyboard templates
    ├── telebot.py                           # Bot runner (Telegram Entry Point)
    └── test.py                              # Session reset utility for test accounts
```

---

### Prerequisites

1.  **Python:** Version 3.10 or higher.
2.  **System Requirements:** The `moviepy` library requires **FFmpeg** to be installed on your system and registered in your system environment PATH variables.
3.  **Python Libraries:**
    ```bash
    pip install instagrapi python-telegram-bot moviepy pillow pyotp pytz arabic-reshaper python-bidi schedule
    ```

---

### Installation & Setup

#### Step 1: Configure Telegram Security Settings
Open `telebot/constants.py` and input the Telegram bot token you received from `@BotFather`, along with the numeric Telegram IDs of authorized administrators:

```python
# telebot/constants.py

# Your Telegram Bot Token
my_token = 'YOUR_TELEGRAM_BOT_TOKEN'

# Authorized Telegram user IDs
my_user_ids = [
    YOUR_TELEGRAM_USER_ID_1,
    YOUR_TELEGRAM_USER_ID_2
]
```

#### Step 2: Start the Telegram Bot (Admin Panel)
Run the Telegram bot to activate the control panel:
```bash
python telebot/telebot.py
```
Go to your bot in Telegram and send `/start`. The interactive custom keyboard options should appear.

#### Step 3: Register an Instagram Account
1. On the bot, navigate to **Account** -> **Add Account**.
2. Provide the Instagram Username.
3. Provide the Password.
4. Provide the 2FA Secret Key (used to dynamically generate security codes at login).
5. The bot validates the credentials and generates an initial session file upon successful login.

#### Step 4: Add Media to Queue & Configure Suffixes
*   **Queuing Content:** Choose **Content** from the menu, select your targeted Instagram profile, and send any photo or video with a caption. The file will be queued under `instabot/downloads/[username]`.
*   **Setting Post Frequency:** Choose **Setting**, select your profile, and determine the daily post frequency (from 0 to 13).
*   **Stitching Captions:** Insert default hashtags or promotional texts to append to the end of your captions.

#### Step 5: Start the Automated Uploader (Instabot)
Keep the scheduler script running continuously on your server (e.g., using PM2 or background screen tools) to process the active timeline:
```bash
python instabot/instabot.py
```
