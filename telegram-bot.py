from telegram.ext import ContextTypes, MessageHandler, filters, ApplicationBuilder, Application
from io import BytesIO
import openai
import requests
import time
import os
import asyncio
from pydub import AudioSegment

# import env variables
from dotenv import load_dotenv
from telegram import Update

from buf import BytesIOWithName
from chat import add_history, chat
load_dotenv()

# import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatBot:
    app: Application = None

    def __init__(self):
        self.app = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_text))
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.app.add_handler(MessageHandler(
            filters.AUDIO | filters.VOICE, self.handle_audio))

    def download_file(self, file_path):
        url = file_path
        filename = file_path.split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        open(f"downloads/{filename}", 'wb').write(r.content)
        return filename

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        task = asyncio.create_task(chat(update.message.text))
        await asyncio.sleep(0)

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=await task)

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Photo received!")

    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # use whisper to transcribe audio

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        # get the audio
        voice = update.message.voice if update.message.voice else update.message.audio
        voice_id = voice.file_id
        voice_file = await context.bot.get_file(voice_id)
        filename = self.download_file(voice_file.file_path)
        ext = filename.split('.')[-1]

        # convert .oga to .mp3
        audio = AudioSegment.from_file(
            f"downloads/{filename}", format="ogg" if ext == "oga" else None)

        # Export the audio to the desired format
        buffer = BytesIO()
        audio.export(buffer, format="mp3")
        file_obj = BytesIOWithName(buffer.getvalue(), "voice.mp3")

        transcript = openai.Audio.transcribe("whisper-1", file_obj)
        add_history("Transcript of file voice.mp3:\n" + transcript["text"])

        # send the transcript back
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Transcript:\n" + transcript["text"])

    def start(self):
        self.app.run_polling()


def main():
    bot = ChatBot()
    bot.start()


if __name__ == '__main__':
    asyncio.run(main())
