from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
import asyncio
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))  # Pastikan CHAT_ID berupa integer
bot = Bot(token=TOKEN)

async def add_buttons(update, context):
    """Menambahkan teks watermark dan tombol ke pesan berisi file APK."""
    message = update.effective_message  # Ambil pesan terbaru, bisa dari channel/grup

    if message and message.document:  # Cek apakah pesan mengandung file (APK)
        watermark_text = "📌 Premium pro applications and modifications only in: @modzilaapk"
        
        # Cek jika caption ada atau tidak, jika tidak, buat string kosong
        new_caption = (message.caption or "") + "\n\n" + watermark_text

        try:
            # Edit pesan untuk menambahkan watermark
            await asyncio.sleep(1)  # Beri jeda biar pesan sudah sepenuhnya dikirim
            await bot.edit_message_caption(
                chat_id=message.chat_id, 
                message_id=message.message_id, 
                caption=new_caption
            )
        except Exception as e:
            print(f"Error edit caption: {e}")  # Debug jika error

        try:
            # Tambahkan tombol watermark
            buttons = [[InlineKeyboardButton("🔹 Modzilla™ 🔹", url="https://t.me/modzilaapk")]]
            reply_markup = InlineKeyboardMarkup(buttons)

            await asyncio.sleep(1)  # Jeda agar edit tidak terlalu cepat
            await bot.edit_message_reply_markup(
                chat_id=message.chat_id, 
                message_id=message.message_id, 
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"Error edit reply markup: {e}")  # Debug jika error

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, add_buttons))

print("Bot sedang berjalan...")
app.run_polling()
