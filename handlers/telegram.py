from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
    ApplicationBuilder,
    Application,
)
from io import BytesIO
import openai
import requests
import os
import asyncio
from pydub import AudioSegment
from sherlock.sherlock import ask_sherlock

from telegram import Update

from util.buf import BytesIOWithName


class ChatBot:
    app: Application

    def __init__(self):
        self.app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_text))
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.app.add_handler(
            MessageHandler(filters.AUDIO | filters.VOICE, self.handle_audio)
        )

    def download_file(self, file_path):
        url = file_path
        filename = file_path.split("/")[-1]
        r = requests.get(url, allow_redirects=True)
        open(f"downloads/{filename}", "wb").write(r.content)
        return filename

    async def respond_to_text(
        self, message: str, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        if update.effective_chat is None:
            # ignore
            return
        
        name = update.effective_chat.full_name

        task = asyncio.create_task(ask_sherlock(message, str(update.effective_chat.id), name))
        asyncio.create_task(
            context.bot.send_chat_action(
                chat_id=update.effective_chat.id, action="typing"
            )
        )
        await asyncio.sleep(0)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=await task
        )

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.respond_to_text(update.message.text, update, context)

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Photo received! 🍄"
        )

    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # use whisper to transcribe audio

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        # get the audio
        voice = update.message.voice if update.message.voice else update.message.audio
        voice_id = voice.file_id
        voice_file = await context.bot.get_file(voice_id)
        filename = self.download_file(voice_file.file_path)
        ext = filename.split(".")[-1]

        # convert .oga to .mp3
        audio = AudioSegment.from_file(
            f"downloads/{filename}", format="ogg" if ext == "oga" else None
        )

        # Export the audio to the desired format
        buffer = BytesIO()
        audio.export(buffer, format="mp3")
        file_obj = BytesIOWithName(buffer.getvalue(), "voice.mp3")

        transcript: dict = openai.Audio.transcribe("whisper-1", file_obj)
        transcript_str: str = transcript["text"]

        # remove file
        os.remove(f"downloads/{filename}")

        # send the transcript back
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Transcript:\n" + transcript_str
        )

        if update.message.voice is not None:
            # respond to the transcript
            await self.respond_to_text(transcript_str, update, context)

    async def start(self):
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()


async def start():
    print("Starting Telegram handler...")
    bot = ChatBot()
    try:
        await bot.start()
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        raise
    finally:
        await bot.app.stop()

