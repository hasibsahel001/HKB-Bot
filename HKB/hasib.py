from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# 🔥 توکن ربات
BOT_TOKEN = '7846991757:AAEZiZFE8lf0VMLXQiveG77B91z_bV_B49s'

# 🔥 آیدی عددی مدیر
ADMIN_ID = 1283450310  # آیدی عددی خودتو اینجا بذار

# لیست کاربران
user_ids = set()

# --- منوی اصلی
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🆘 نیاز به کمک دارم", callback_data='help')],
    ]
    return InlineKeyboardMarkup(keyboard)

# --- منوی کمک
def help_menu():
    keyboard = [
        [InlineKeyboardButton("📲 راه‌اندازی اپلیکیشن هندوکش بریج", callback_data='setup_app')],
        [InlineKeyboardButton("🔐 تغییر پسورد وای‌فای", callback_data='change_wifi_password')],
        [InlineKeyboardButton("➕ سایر درخواست‌ها", callback_data='other_requests')],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data='back_to_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

# --- فرمان /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_ids.add(user_id)
    await update.message.reply_text(
        "سلام! به ربات خدمات خوش آمدید.\n\nبرای دریافت خدمات از دکمه‌های زیر استفاده کنید 👇",
        reply_markup=main_menu()
    )

# --- مدیریت دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        await query.edit_message_text(
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید 👇",
            reply_markup=help_menu()
        )
    elif query.data == 'setup_app':
        await query.edit_message_text(
            "✅ راه‌اندازی اپلیکیشن هند‌کش بریج:\n\n"
            "1- اپلیکیشن را دانلود کنید.\n"
            "2- روی گوشی نصب کنید.\n"
            "3- اطلاعات اتصال را وارد نمایید."
        )
    elif query.data == 'change_wifi_password':
        await query.edit_message_text(
            "🔐 آموزش تغییر پسورد وای‌فای:\n\n"
            "1- وارد تنظیمات مودم شوید.\n"
            "2- به قسمت Wireless بروید.\n"
            "3- رمز جدید را وارد کنید و ذخیره نمایید."
        )
    elif query.data == 'other_requests':
        await query.edit_message_text(
            "➕ لطفاً درخواست خود را به صورت متنی ارسال نمایید.\n"
            "کارشناس ما در اولین فرصت پاسخ خواهد داد."
        )
    elif query.data == 'back_to_main':
        await query.edit_message_text(
            "🏠 بازگشت به منوی اصلی",
            reply_markup=main_menu()
        )

# --- فرمان /broadcast برای مدیر
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ شما اجازه‌ی ارسال پیام به همه را ندارید.")
        return

    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("✏️ لطفاً متنی که باید ارسال شود را وارد کنید.")
        return

    success_count = 0
    for user_id in user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=text, reply_markup=main_menu())
            success_count += 1
        except Exception as e:
            print(f"خطا در ارسال به {user_id}: {e}")

    await update.message.reply_text(f"✅ پیام به {success_count} کاربر ارسال شد.")

# --- اجرای ربات
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 ربات با موفقیت شروع شد...")
    app.run_polling()

if __name__ == '__main__':
    main()
