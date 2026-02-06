from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from PIL import Image  # imghdr replacement

# ===== CONFIG =====
BOT_TOKEN = None  # Railway Environment variable se lega
UPI_ID = None     # Railway Environment variable se lega
ADMIN_CHAT_ID = None  # Railway Environment variable se lega

# ===== PACKAGES =====
PACKAGES = (
    "💎 *Choose a package 👇*\n\n"
    "1️⃣ ₹499  – 999 Diamonds\n"
    "2️⃣ ₹1999 – 4999 Diamonds\n"
    "3️⃣ ₹4999 – 14999 Diamonds\n"
    "4️⃣ ₹9999 – 29999 Diamonds\n"
)

PAYMENT_MSG_TEMPLATE = (
    "💳 *Payment Details*\n\n"
    "🔹 *UPI ID:* `{upi_id}`\n\n"
    "✅ Payment karne ke baad *screenshot bhejo*.\n\n"
    "⏳ Payment jaldi hi processing complete karega.\n"
    "💎 24 hours ke andar diamonds mil jaayenge."
)

UNDER_REVIEW = (
    "🕐 *Payment Under Review*\n\n"
    "Screenshot mil gaya hai.\n"
    "Ab *Game ID* bhejo."
)

FINAL_MSG = (
    "✅ *Payment Processing Started*\n\n"
    "Agar payment verify ho gaya to\n"
    "⏳ 24 hours ke andar diamonds credit ho jaayenge.\n\n"
    "Thanks for buying ❤️"
)

# ===== HANDLERS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🛒 BUY", callback_data="buy")]]
    await update.message.reply_text(
        "Welcome 👋\nDiamond Store Bot",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    # Buttons for each package separately
    keyboard = [
        [InlineKeyboardButton("₹499 – 999 Diamonds", callback_data="p1")],
        [InlineKeyboardButton("₹1999 – 4999 Diamonds", callback_data="p2")],
        [InlineKeyboardButton("₹4999 – 14999 Diamonds", callback_data="p3")],
        [InlineKeyboardButton("₹9999 – 29999 Diamonds", callback_data="p4")]
    ]
    await q.edit_message_text(
        PACKAGES,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def pay_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    package_map = {
        "p1": "₹499 – 999 Diamonds",
        "p2": "₹1999 – 4999 Diamonds",
        "p3": "₹4999 – 14999 Diamonds",
        "p4": "₹9999 – 29999 Diamonds",
    }
    selected = package_map.get(q.data, "Unknown Package")
    # Payment message with correct UPI
    await q.edit_message_text(
        PAYMENT_MSG_TEMPLATE.format(upi_id=UPI_ID) + f"\n\nSelected Package: {selected}",
        parse_mode="Markdown"
    )

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Forward screenshot to admin
    await context.bot.forward_message(
        chat_id=int(ADMIN_CHAT_ID),
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )
    context.user_data["wait_game_id"] = True
    await update.message.reply_text(UNDER_REVIEW, parse_mode="Markdown")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("wait_game_id"):
        game_id = update.message.text
        await context.bot.send_message(
            int(ADMIN_CHAT_ID),
            f"🎮 Game ID Received:\n{game_id}\nUser: @{update.message.from_user.username}"
        )
        context.user_data["wait_game_id"] = False
        await update.message.reply_text(FINAL_MSG, parse_mode="Markdown")

# ===== MAIN =====
def main():
    import os
    global BOT_TOKEN, UPI_ID, ADMIN_CHAT_ID
    # Get values from Railway Environment Variables
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    UPI_ID = os.environ.get("UPI_ID")
    ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buy, pattern="^buy$"))
    app.add_handler(CallbackQueryHandler(pay_package, pattern="^p[1-4]$"))
    app.add_handler(MessageHandler(filters.PHOTO, screenshot))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

    

   

    

    
       
