import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from moviepy.editor import VideoFileClip

TOKEN = os.getenv("TOKEN")

async def video_to_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.video:
            await update.message.reply_text("Отправь видео")
            return

        video = await update.message.video.get_file()

        await video.download_to_drive("video.mp4")

        clip = VideoFileClip("video.mp4")
        clip.audio.write_audiofile("audio.mp3")
        clip.close()

        with open("audio.mp3", "rb") as f:
            await update.message.reply_audio(f)

    except Exception as e:
        await update.message.reply_text(str(e))

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.VIDEO, video_to_audio)
)

app.run_polling()
