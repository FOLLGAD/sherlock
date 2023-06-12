import pvporcupine
import sounddevice as sd
import os
import numpy as np
import speech_recognition as sr
import queue
import sys

# source .env
from dotenv import load_dotenv
load_dotenv()

SERVER = sys.argv[1]

ACCESS_KEY = os.environ["PORCUPINE_KEY"]

porcupine = pvporcupine.create(
  access_key=ACCESS_KEY,
  keyword_paths=['./keywords/Sherlock.ppn']
)

mic = sd.InputStream(samplerate=porcupine.sample_rate, channels=1, dtype=np.int16)

# Start the microphone

r = sr.Recognizer()
import requests

def transcribe_command():
    mic.start()
    audio_queue = queue.Queue(maxsize=32)

    # obtain audio from the microphone
    while True:
        frames, overflowed = mic.read(porcupine.frame_length)
        if overflowed:
            print('Audio buffer has overflowed')
            continue
        framesint = frames.flatten().astype(np.int16)  # Flatten to 1D and ensure data is int16
        result = porcupine.process(framesint)

        if audio_queue.full():
            audio_queue.get()
        audio_queue.put(framesint)

        if result >= 0:
            print('Wake word detected!')
            break
    mic.stop()

    with sr.Microphone(sample_rate=porcupine.sample_rate) as source:
        print("Listening for command...")
        audio = r.listen(source)
        # save audio to file
        with open("test-orig.wav", "wb") as f:
            f.write(audio.get_wav_data())
        # append audio_frames to audio
        b = audio.get_raw_data()
        
        # add the prev 16 frames to audio
        audio_frames = list(audio_queue.queue)
        for frame in reversed(audio_frames):
            b = frame.tobytes() + b
        audio = sr.AudioData(b, audio.sample_rate, audio.sample_width)
        # save to file
        with open("test.wav", "wb") as f:
            f.write(audio.get_wav_data())
        command = r.recognize_whisper_api(audio)
        # make http request to localhost:8000 with command
        res = requests.post(f"{SERVER}/sherlock", json={
            "input": command,
            "user_id": 1,
            "user_name": "User",
        })
        print(res.json())
    
    return command

while True:
    command = transcribe_command()
    print(command)
