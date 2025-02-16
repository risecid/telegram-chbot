GNU nano 8.3                             bot.py
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
import time

TOKEN = "1238817594:AAERSGFlgsTT0wchCnuVCFijUIUcgvPPc5A"
CHAT_ID = "-1001444745539"  # Ganti dengan chat ID channel kamu

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
        bot.edit_message_reply_markup(chat_id=CHAT_ID, message_id=message.message_id, r>

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# Handler untuk mendeteksi pesan baru di channel
dp.add_handler(MessageHandler(Filters.document, add_buttons))

print("Bot sedang berjalan...")
updater.start_polling()
updater.idle()
