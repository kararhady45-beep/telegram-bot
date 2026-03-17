import requests
import tempfile
import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔑 حط التوكن هنا
BOT_TOKEN = "8096135136:AAF86cgGs6p8Rb2ugJu7WWNnhF2UzJxSYPw"


def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""

    if "youtube.com" not in text and "youtu.be" not in text:
        await update.message.reply_text("دز رابط يوتيوب مباشر")
        return

    video_id = extract_video_id(text)

    if not video_id:
        await update.message.reply_text("رابط غير صالح")
        return

    await update.message.reply_text("جاري التحويل...")

    try:
        # 🔥 API يشبه YTMP3
        api = "https://api.y2mate.is/v1/convert"

        payload = {
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "format": "mp3"
        }

        res = requests.post(api, json=payload, timeout=30)
        data = res.json()

        if "link" not in data:
            await update.message.reply_text("فشل التحويل")
            return

        download_url = data["link"]

        # 📥 تحميل الصوت
        r = requests.get(download_url, stream=True, timeout=60)
        file_path = os.path.join(tempfile.gettempdir(), "song.mp3")

        with open(file_path, "wb") as f:
            for chunk in r.iter_content(1024 * 256):
                if chunk:
                    f.write(chunk)

        with open(file_path, "rb") as audio:
            await update.message.reply_audio(audio=audio)

        os.remove(file_path)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("صار خطأ")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()