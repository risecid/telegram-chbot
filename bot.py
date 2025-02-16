from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHANNEL_USERNAME = "@modzilaapk"  # Ganti dengan username channel kamu
WATERMARK_TEXT = f"📌 Premium pro applications and modifications only in: {CHANNEL_USERNAME}"

bot = Bot(token=TOKEN)

async def add_buttons(update, context):
    """Menambahkan teks watermark dan tombol ke pesan berisi file APK."""
    message = update.channel_post  # Ambil pesan yang baru dikirim di channel
    if message and message.document:  # Cek apakah pesan mengandung file (APK)
        
        # Edit pesan untuk menambahkan watermark
        new_caption = (message.caption or "") + f"\n\n{WATERMARK_TEXT}"
        await bot.edit_message_caption(
            chat_id=CHAT_ID, 
            message_id=message.message_id, 
            caption=new_caption
        )

        # Tambahkan tombol watermark
        buttons = [[InlineKeyboardButton("🔹 Modzilla™ 🔹", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]]
        reply_markup = InlineKeyboardMarkup(buttons)

        # Edit pesan untuk menambahkan tombol
        await bot.edit_message_reply_markup(chat_id=CHAT_ID, message_id=message.message_id, reply_markup=reply_markup)

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, add_buttons))

if __name__ == "__main__":
    print("Bot Auto Watermark berjalan...")
    app.run_polling()
