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

    # يشتغل فقط على امر يوت
    if not text.startswith("يوت"):
        return

    query = text.replace("يوت", "", 1).strip()

    if not query:
        await update.message.reply_text("اكتب اسم الاغنية بعد يوت")
        return

    await update.message.reply_text("🔍 جاري البحث...")

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "cookiefile": "cookies.txt",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)

            if not info or "entries" not in info or not info["entries"]:
                await update.message.reply_text("ما لكيت نتائج")
                return

            video = info["entries"][0]
            filename = ydl.prepare_filename(video)

            title = video.get("title", "Unknown")[:60]
            duration = int(video.get("duration", 0) or 0)
            performer = (video.get("uploader") or video.get("channel") or "YouTube")[:60]

        if not os.path.exists(filename):
            await update.message.reply_text("صار خطأ بالتحميل")
            return

        with open(filename, "rb") as audio:
            await update.message.reply_audio(
                audio=audio,
                title=title,
                performer=performer,
                duration=duration
            )

        os.remove(filename)

    except Exception as e:
        print("ERROR:", repr(e))
        await update.message.reply_text(f"❌ الخطأ:\n{str(e)[:3000]}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
