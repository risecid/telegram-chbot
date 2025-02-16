from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import asyncio
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

async def process_message(context: ContextTypes.DEFAULT_TYPE):
    """Proses penambahan watermark & tombol dengan delay supaya tidak ada yang terlewat."""
    job_data = context.job.data  # Ambil data dari job queue
    message = job_data["message"]
    bot = job_data["bot"]

    watermark_text = "📌 Premium pro applications and modifications only in: @modzilaapk"

    # Edit pesan untuk menambahkan watermark
    new_caption = (message.caption or "") + "\n\n" + watermark_text
    await bot.edit_message_caption(
        chat_id=message.chat_id, 
        message_id=message.message_id, 
        caption=new_caption
    )

    # Tambahkan tombol watermark
    buttons = [[InlineKeyboardButton("🔹 Modzilla™ 🔹", url="https://t.me/modzilaapk")]]
    reply_markup = InlineKeyboardMarkup(buttons)

    await asyncio.sleep(2)  # Delay tambahan untuk mencegah spam request
    await bot.edit_message_reply_markup(chat_id=message.chat_id, message_id=message.message_id, reply_markup=reply_markup)

async def add_buttons(update, context):
    """Tambahkan pesan ke job queue supaya tidak ada yang terlewat."""
    message = update.channel_post
    if message and message.document:
        context.job_queue.run_once(process_message, when=2, data={"message": message, "bot": context.bot})

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, add_buttons))

print("Bot sedang berjalan...")
app.run_polling()
