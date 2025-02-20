from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
import asyncio
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
bot = Bot(token=TOKEN)

async def add_buttons(update, context):
    """Menambahkan tombol ke pesan setelah watermark ditambahkan."""
    message = update.effective_message

    if message and message.document:
        await asyncio.sleep(5)  # Tunggu lebih lama agar caption pasti teredit

        try:
            buttons = [[InlineKeyboardButton("🔹 Modzilla™ 🔹", url="https://t.me/modzilaapk")]]
            reply_markup = InlineKeyboardMarkup(buttons)

            await bot.edit_message_reply_markup(
                chat_id=message.chat_id,
                message_id=message.message_id,
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"Error edit reply markup: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, add_buttons))

print("Bot Tombol sedang berjalan...")
app.run_polling()
