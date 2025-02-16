import os
import time
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Ambil TOKEN & Chat ID dari Environment Variables
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Inisialisasi Bot
bot = Bot(token=TOKEN)

async def add_buttons(update: Update, context: CallbackContext):
    """Menambahkan tombol Like & Dislike ke pesan baru di channel."""
    message = update.channel_post  # Ambil pesan yang baru dikirim di channel

    if message and message.document:  # Cek apakah pesan mengandung file (APK)
        buttons = [[
            InlineKeyboardButton("👍", callback_data="like"),
            InlineKeyboardButton("👎", callback_data="dislike")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)

        # Tunggu sebentar agar pesan terkirim dulu
        time.sleep(1)

        # Edit pesan untuk menambahkan tombol
        await bot.edit_message_reply_markup(chat_id=CHAT_ID, message_id=message.message_id, reply_markup=reply_markup)

async def button_callback(update: Update, context: CallbackContext):
    """Menangani klik tombol Like & Dislike"""
    query = update.callback_query
    await query.answer()

    if query.data == "like":
        await query.edit_message_text(text="👍 Anda menyukai ini!")
    elif query.data == "dislike":
        await query.edit_message_text(text="👎 Anda tidak menyukai ini!")

def main():
    """Main function untuk menjalankan bot"""
    app = Application.builder().token(TOKEN).build()

    # Handler untuk pesan baru di channel
    app.add_handler(MessageHandler(filters.Document.ALL, add_buttons))

    print("Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
