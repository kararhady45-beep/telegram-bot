import yt_dlp
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8096135136:AAF86cgGs6p8Rb2ugJu7WWNnhF2UzJxSYPw"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    # تحقق انه رابط يوتيوب
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("دز رابط يوتيوب مباشر")
        return

    await update.message.reply_text("جاري التحويل...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'quiet': True,
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # ارسال الصوت
        with open(filename, "rb") as audio:
            await update.message.reply_audio(audio=audio)

        # حذف الملف بعد الارسال
        os.remove(filename)

    except Exception as e:
        print("ERROR:", repr(e))
        await update.message.reply_text(f"الخطأ:\n{str(e)[:3000]}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
