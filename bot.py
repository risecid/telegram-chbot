from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
import asyncio
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))  # Pastikan CHAT_ID berupa integer
bot = Bot(token=TOKEN)

async def add_buttons(update, context):
    """Menambahkan teks watermark dan tombol ke pesan berisi file APK."""
    message = update.effective_message  

    if message and message.document:  # Cek apakah pesan mengandung file (APK)
        watermark_text = "📌 Premium pro applications and modifications only in: @modzilaapk"
        new_caption = (message.caption or "") + "\n\n" + watermark_text

        buttons = [[InlineKeyboardButton("🔹 Modzilla™ 🔹", url="https://t.me/modzilaapk")]]
        reply_markup = InlineKeyboardMarkup(buttons)

        await asyncio.sleep(5)  # Tambahkan delay agar tidak terlalu cepat

        try:
            await bot.edit_message_caption(
                chat_id=message.chat_id, 
                message_id=message.message_id, 
                caption=new_caption,
                reply_markup=reply_markup,  # Tambahkan tombol di sini langsung
                parse_mode="HTML"
            )
            print("Caption & Tombol berhasil ditambahkan")
        except Exception as e:
            print(f"Error edit caption & tombol: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, add_buttons))

print("Bot sedang berjalan...")
app.run_polling()
