import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# حط توكن البوت هنا
TOKEN = "8096135136:AAF86cgGs6p8Rb2ugJu7WWNnhF2UzJxSYPw"


async def post_init(application):
    try:
        await application.bot.delete_webhook(drop_pending_updates=True)
        print("Webhook deleted successfully")
    except Exception as e:
        print(f"Webhook delete error: {e}")


def get_performer(video_info: dict) -> str:
    return (
        video_info.get("artist")
        or video_info.get("uploader")
        or video_info.get("channel")
        or "YouTube"
    )[:64]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if not text.startswith("يوت"):
        return

    query = text.replace("يوت", "", 1).strip()

    if not query:
        await update.message.reply_text("اكتب اسم الاغنية بعد يوت")
        return

    wait_msg = await update.message.reply_text("🔍 جاري البحث...")

    filename = None

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "default_search": "ytsearch1",
        }

        if os.path.exists("cookies.txt"):
            ydl_opts["cookiefile"] = "cookies.txt"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)

            if "entries" in info and info["entries"]:
                video = info["entries"][0]
            else:
                video = info

            filename = ydl.prepare_filename(video)

        if not filename or not os.path.exists(filename):
            await wait_msg.edit_text("صار خطأ بالتحميل")
            return

        title = (video.get("title") or "Unknown")[:64]
        duration = int(video.get("duration") or 0)
        performer = get_performer(video)

        with open(filename, "rb") as audio_file:
            await update.message.reply_audio(
                audio=audio_file,
                title=title,
                performer=performer,
                duration=duration,
            )

        await wait_msg.delete()

    except Exception as e:
        print("ERROR:", repr(e))
        await wait_msg.edit_text(f"❌ الخطأ:\n{str(e)[:2000]}")

    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception:
                pass


def main():
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot running...")
    app.run_polling(drop_pending_updates=True, close_loop=False)


if __name__ == "__main__":
    main()
