from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
import os
import asyncio
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHANNEL_USERNAME = "@modzilaapk"
WATERMARK_TEXT = f"📌 Premium pro applications and modifications only in: {CHANNEL_USERNAME}"

bot = Bot(token=TOKEN)

async def get_image_url(app_name):
    """Cari gambar dari DuckDuckGo berdasarkan nama APK."""
    search_url = f"https://duckduckgo.com/?q={app_name}+logo&t=h_&iar=images"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        image_elements = soup.select("img[src]")
        
        for img in image_elements:
            img_url = img["src"]
            if "https://" in img_url:  # Pastikan URL valid
                return img_url
    except Exception as e:
        print(f"Error mencari gambar: {e}")
    
    return None

async def process_message(update, context):
    """Menambahkan teks watermark, tombol, dan thumbnail ke pesan berisi file APK."""
    message = update.channel_post
    if message and message.document:
        app_name = message.document.file_name.split(".apk")[0]  # Ambil nama file tanpa .apk
        
        # Cari gambar dari DuckDuckGo
        image_url = await get_image_url(app_name)
        
        # Edit caption tambahkan watermark
        new_caption = (message.caption or "") + f"\n\n{WATERMARK_TEXT}"
        await bot.edit_message_caption(
            chat_id=CHAT_ID, 
            message_id=message.message_id, 
            caption=new_caption
        )

        # Tambahkan tombol watermark
        buttons = [[InlineKeyboardButton("🔹 Modzilla™ 🔹", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await bot.edit_message_reply_markup(chat_id=CHAT_ID, message_id=message.message_id, reply_markup=reply_markup)

        # Kirim gambar sebagai thumbnail jika ditemukan
        if image_url:
            await bot.send_photo(chat_id=CHAT_ID, photo=image_url, caption=f"🔹 {app_name} 🔹")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, process_message))

if __name__ == "__main__":
    print("Bot Auto Thumbnail berjalan...")
    app.run_polling()
