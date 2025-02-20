from telegram import Bot
from telegram.ext import Application, MessageHandler, filters
import asyncio
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
bot = Bot(token=TOKEN)

async def add_watermark(update, context):
    """Menambahkan teks watermark ke pesan berisi file APK."""
    message = update.effective_message

    if message and message.document:
        watermark_text = "📌 Premium pro applications and modifications only in: @modzilaapk"
        new_caption = (message.caption or "") + "\n\n" + watermark_text

        try:
            await asyncio.sleep(1)  # Pastikan pesan sudah terkirim
            await bot.edit_message_caption(
                chat_id=message.chat_id,
                message_id=message.message_id,
                caption=new_caption
            )
        except Exception as e:
            print(f"Error edit caption: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, add_watermark))

print("Bot Caption sedang berjalan...")
app.run_polling()
