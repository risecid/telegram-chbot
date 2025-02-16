import os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, filters, CallbackContext

# Ambil TOKEN dari environment variables (Railway)
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

def send_post(update: Update, context: CallbackContext):
    """Mengirim pesan dengan tombol Like & Dislike"""
    message = update.channel_post  # Ambil pesan dari channel
    keyboard = [
        [InlineKeyboardButton("👍 Like", callback_data="like"),
         InlineKeyboardButton("👎 Dislike", callback_data="dislike")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=message.chat_id,
        text=message.text if message.text else "File baru!",
        reply_markup=reply_markup
    )

def button_callback(update: Update, context: CallbackContext):
    """Menangani tombol Like & Dislike"""
    query = update.callback_query
    query.answer()

    if query.data == "like":
        query.edit_message_text(text="👍 Anda menyukai ini!")
    elif query.data == "dislike":
        query.edit_message_text(text="👎 Anda tidak menyukai ini!")

# Setup bot
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# Tangkap pesan baru di channel & tambahkan tombol
dp.add_handler(MessageHandler(filters.ALL, send_post))

# Tangkap tombol yang ditekan
dp.add_handler(CallbackQueryHandler(button_callback))

print("Bot berjalan...")
updater.start_polling()
updater.idle()
