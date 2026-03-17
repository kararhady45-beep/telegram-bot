import yt_dlp
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# حط التوكن هنا
TOKEN = "8096135136:AAF86cgGs6p8Rb2ugJu7WWNnhF2UzJxSYPw"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if not text.startswith("يوت"):
        return

    query = text.replace("يوت", "").strip()

    if not query:
        await update.message.reply_text("اكتب اسم الاغنية بعد يوت")
        return

    await update.message.reply_text("🔍 جاري البحث...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            video = info['entries'][0]

            filename = ydl.prepare_filename(video)
            title = video.get('title', 'Unknown')[:60]
            duration = video.get('duration', 0)

        with open(filename, "rb") as audio:
            await update.message.reply_audio(
                audio=audio,
                title=title,
                performer="YouTube",
                duration=duration
            )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ خطأ:\n{str(e)[:2000]}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
