import os
from openai import OpenAI
from gtts import gTTS
import pygame
import io
import threading
import time

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-JoABD96Rui1GWSrpJ6h78lTDEkbQG386TWBYZWLPQHoWewkU"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.opentyphoon.ai/v1",
)

# Initialize pygame mixer
pygame.mixer.init()

def text_to_speech_and_play(text):
    tts = gTTS(text, lang='th')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.01)

def wait_and_process_chunks(stream):
    buffer = ""
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content
        if chunk_message:
            print(f"{chunk_message}", end="", flush=True)
            buffer += chunk_message
            if len(buffer) >= 128 or any(p in buffer for p in ".!?"):
                text_to_speech_and_play(buffer)
                buffer = ""
        time.sleep(0.01)  # Small delay to allow for speech to catch up

    # Process any remaining text
    if buffer:
        text_to_speech_and_play(buffer)

stream = client.chat.completions.create(
    model="typhoon-v1.5x-70b-instruct",
    messages=[
        {
            "role": "user",
            "content": "คุณเป็นใคร ทำอะไรได้บ้าง",
        }
    ],
    max_tokens=512,
    temperature=0.6,
    top_p=0.95,
    stream=True,
)

# Start processing in a separate thread
threading.Thread(target=wait_and_process_chunks, args=(stream,)).start()

# Wait for the thread to finish
while threading.active_count() > 1:
    time.sleep(0.01)

print("\nGeneration and playback complete.")