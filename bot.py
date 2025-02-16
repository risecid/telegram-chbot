from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
import time

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

def add_buttons(update, context):
    """Menambahkan tombol Like & Dislike ke pesan baru di channel."""
    message = update.channel_post  # Ambil pesan yang baru dikirim di channel
    if message.document:  # Cek apakah pesan mengandung file (APK)
        buttons = [[
            InlineKeyboardButton("👍", callback_data="like"),
            InlineKeyboardButton("👎", callback_data="dislike")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)

        # Edit pesan untuk menambahkan tombol
        time.sleep(1)  # Tunggu sebentar biar pesan terkirim dulu
        bot.edit_message_reply_markup(chat_id=CHAT_ID, message_id=message.message_id, reply_markup=reply_>

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# Handler untuk mendeteksi pesan baru di channel
dp.add_handler(MessageHandler(Filters.document, add_buttons))

print("Bot sedang berjalan...")
updater.start_polling()
updater.idle()
