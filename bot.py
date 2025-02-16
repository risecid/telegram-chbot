import os
import time
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters, CallbackContext

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

async def add_buttons(update: Update, context: CallbackContext):
    """Menambahkan tombol Like & Dislike ke pesan baru di channel."""
    message = update.channel_post  

    if message and message.document:
        buttons = [[
            InlineKeyboardButton("👍 0", callback_data="like_0"),
            InlineKeyboardButton("👎 0", callback_data="dislike_0")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)

        time.sleep(1)
        await bot.edit_message_reply_markup(chat_id=CHAT_ID, message_id=message.message_id, reply_markup=reply_markup)

async def button_callback(update: Update, context: CallbackContext):
    """Menangani klik tombol Like & Dislike"""
    query = update.callback_query
    await query.answer()  # Ini penting biar tombol tidak muter terus

    # Ambil data tombol & hitung jumlah vote
    data = query.data.split("_")  
    action = data[0]  
    count = int(data[1]) + 1  

    # Update teks tombol dengan jumlah baru
    if action == "like":
        new_buttons = [[
            InlineKeyboardButton(f"👍 {count}", callback_data=f"like_{count}"),
            InlineKeyboardButton(f"👎 {data[1]}", callback_data=f"dislike_{data[1]}")
        ]]
    else:
        new_buttons = [[
            InlineKeyboardButton(f"👍 {data[1]}", callback_data=f"like_{data[1]}"),
            InlineKeyboardButton(f"👎 {count}", callback_data=f"dislike_{count}")
        ]]

    reply_markup = InlineKeyboardMarkup(new_buttons)

    # Update tombol di pesan
    await query.edit_message_reply_markup(reply_markup=reply_markup)

def main():
    """Main function untuk menjalankan bot"""
    app = Application.builder().token(TOKEN).build()

    # Handler untuk pesan baru di channel
    app.add_handler(MessageHandler(filters.Document.ALL, add_buttons))
    
    # Handler untuk menangani klik tombol
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
