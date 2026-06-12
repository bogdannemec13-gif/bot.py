import asyncio
import os
import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
import yt_dlp

TOKEN = os.getenv("8724847696:AAGZoj7nPJceo8kVSIkxyU03ReVYNVQwvyA")

bot = Bot(token=TOKEN)
dp = Dispatcher()

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def download_audio(url: str) -> str:
    file_id = str(uuid.uuid4())

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/{file_id}.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)

    return f"{DOWNLOAD_FOLDER}/{file_id}.mp3"


@dp.message()
async def handler(message: types.Message):
    if not message.text or not message.text.startswith("http"):
        await message.answer("Отправь ссылку на видео")
        return

    await message.answer("⏳ Скачиваю и конвертирую...")

    try:
        path = download_audio(message.text)
        audio = FSInputFile(path)

        await message.answer_audio(audio)

        os.remove(path)

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
