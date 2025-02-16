from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
import asyncio
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

async def add_buttons(update, context):
    """Menambahkan tombol watermark dengan nama channel."""
    message = update.channel_post  # Ambil pesan yang baru dikirim di channel
    if message and message.document:  # Cek apakah pesan mengandung file (APK)
        buttons = [[InlineKeyboardButton("🔹 Modzilla™ 🔹", url="https://t.me/modzilaapk")]]
        reply_markup = InlineKeyboardMarkup(buttons)

        await asyncio.sleep(1)  # Tunggu sebentar biar pesan terkirim dulu
        await bot.edit_message_reply_markup(chat_id=CHAT_ID, message_id=message.message_id, reply_markup=reply_markup)

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, add_buttons))

print("Bot sedang berjalan...")
app.run_polling()
