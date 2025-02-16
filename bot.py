from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
import os
import asyncio

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHANNEL_USERNAME = "@modzilaapk"  # Ganti dengan username channel kamu
WATERMARK_TEXT = f"📌 Premium pro applications and modifications only in: {CHANNEL_USERNAME}"

bot = Bot(token=TOKEN)
queue = asyncio.Queue()  # Buat antrean untuk memproses pesan satu per satu

async def process_queue():
    """Memproses pesan dalam antrean satu per satu"""
    while True:
        update = await queue.get()
        await process_message(update)
        queue.task_done()

async def process_message(update):
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

async def add_to_queue(update, context):
    """Menambahkan pesan ke dalam antrean untuk diproses"""
    await queue.put(update)

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, add_to_queue))

# Jalankan pemrosesan antrean secara paralel
loop = asyncio.get_event_loop()
loop.create_task(process_queue())

if __name__ == "__main__":
    print("Bot Auto Watermark berjalan...")
    app.run_polling()
