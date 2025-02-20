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
        new_caption = (message.caption or "") + "\n\n" + watermark_text

        # Tambahkan delay agar tidak terlalu cepat
        await asyncio.sleep(5)  

        try:
            # Cek apakah caption sudah mengandung watermark, agar tidak diedit ulang
            if watermark_text not in (message.caption or ""):
                await bot.edit_message_caption(
                    chat_id=message.chat_id, 
                    message_id=message.message_id, 
                    caption=new_caption,
                    parse_mode="HTML"
                )
                print("Caption berhasil diedit")
            else:
                print("Caption sudah ada, tidak perlu diedit")
        except Exception as e:
            print(f"Error edit caption: {e}")  # Debug jika error

        try:
            # Tambahkan tombol watermark
            buttons = [[InlineKeyboardButton("🔹 Modzilla™ 🔹", url="https://t.me/modzilaapk")]]
            reply_markup = InlineKeyboardMarkup(buttons)

            await asyncio.sleep(3)  # Tambahkan delay sebelum edit tombol
            await bot.edit_message_reply_markup(
                chat_id=message.chat_id, 
                message_id=message.message_id, 
                reply_markup=reply_markup
            )
            print("Tombol berhasil ditambahkan")
        except Exception as e:
            print(f"Error edit reply markup: {e}")  # Debug jika error

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, add_buttons))

print("Bot sedang berjalan...")
app.run_polling()
