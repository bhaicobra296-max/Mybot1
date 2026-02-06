from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ========== CONFIG ==========
BOT_TOKEN = "8144899871:AAE7xErlB0dpV7wbRR8VhT5ZqiWFLFA2BiI"
UPI_ID = "payengsiyokistorez@fam"
ADMIN_CHAT_ID = 7767054180
# ============================

PACKAGES = {
    "p499": ("₹499", "999 Diamonds"),
    "p1999": ("₹1999", "4999 Diamonds"),
    "p4999": ("₹4999", "14999 Diamonds"),
    "p9999": ("₹9999", "29999 Diamonds"),
}

# ===== HANDLERS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Buy Diamonds", callback_data="buy")]
    ]
    await update.message.reply_text(
        "Welcome 👋\n💎 Diamond Store Bot",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    keyboard = [
        [InlineKeyboardButton("₹499 – 999 Diamonds", callback_data="p499")],
        [InlineKeyboardButton("₹1999 – 4999 Diamonds", callback_data="p1999")],
        [InlineKeyboardButton("₹4999 – 14999 Diamonds", callback_data="p4999")],
        [InlineKeyboardButton("₹9999 – 29999 Diamonds", callback_data="p9999")],
    ]

    await q.edit_message_text(
        "💎 *Choose a package 👇*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def package_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    price, diamonds = PACKAGES[q.data]
    context.user_data["selected_price"] = price

    text = (
        "✅ *Package Selected*\n\n"
        f"💰 Price: *{price}*\n"
        f"💎 Diamonds: *{diamonds}*\n\n"
        "💳 *Payment Details*\n"
        f"🔹 UPI ID: `{UPI_ID}`\n\n"
        f"👉 Is UPI ID par *{price}* pay karke "
        "*payment ka screenshot bhej dijiye*.\n\n"
        "⏳ Payment verify hone ke baad\n"
        "💎 Diamonds 24 hours ke andar mil jaayenge."
    )

    await q.edit_message_text(text, parse_mode="Markdown")

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "selected_price" not in context.user_data:
        await update.message.reply_text("❌ Pehle package select karo.")
        return

    await context.bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id,
    )

    context.user_data["wait_game_id"] = True

    await update.message.reply_text(
        "🕐 *Payment Under Review*\n\n"
        "Screenshot mil gaya hai ✅\n"
        "Ab apni *Game ID* bhejo.",
        parse_mode="Markdown",
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("wait_game_id"):
        game_id = update.message.text

        await context.bot.send_message(
            ADMIN_CHAT_ID,
            f"🎮 Game ID Received\n\n"
            f"Game ID: {game_id}\n"
            f"User: @{update.message.from_user.username}"
        )

        context.user_data["wait_game_id"] = False

        await update.message.reply_text(
            "✅ *Payment Processing Started*\n\n"
            "Agar payment verify ho gaya to\n"
            "⏳ 24 hours ke andar diamonds mil jaayenge.\n\n"
            "Thanks for buying ❤️",
            parse_mode="Markdown",
        )

# ===== MAIN =====

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buy, pattern="^buy$"))
    app.add_handler(CallbackQueryHandler(package_select, pattern="^p"))
    app.add_handler(MessageHandler(filters.PHOTO, screenshot))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
