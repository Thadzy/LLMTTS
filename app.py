import os
import asyncio
import edge_tts
import pygame
import io
import threading
import queue
from openai import OpenAI
from thai_tokenizer import Tokenizer

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = ""
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.opentyphoon.ai/v1",
)

# Initialize pygame mixer and Thai tokenizer
pygame.mixer.init()
tokenizer = Tokenizer()

# Create a queue for audio chunks
audio_queue = queue.Queue()

# List of EdgeTTS voices to try
VOICES = ["th-TH-NiwatNeural", "th-TH-PremwadeeNeural", "en-US-ChristopherNeural"]

async def text_to_speech(text):
    for voice in VOICES:
        try:
            communicate = edge_tts.Communicate(text, voice)
            audio_data = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data.write(chunk["data"])
            audio_data.seek(0)
            return audio_data
        except edge_tts.exceptions.NoAudioReceived:
            print(f"Failed to generate audio with voice {voice}. Trying next voice...")
    
    print("All voices failed. Unable to generate audio.")
    return None

def play_audio():
    while True:
        audio = audio_queue.get()
        if audio is None:
            break
        if audio != "skip":
            pygame.mixer.music.load(audio)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        audio_queue.task_done()

async def stream_and_speak():
    buffer = ""
    stream = client.chat.completions.create(
        model="typhoon-v1.5x-70b-instruct",
        messages=[
            {
                "role": "user",
                "content": "วันนี้กินข้าวกับอะไรดี",
            }
        ],
        max_tokens=512,
        temperature=0.6,
        top_p=0.95,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end='', flush=True)
            buffer += content
            
            # Check if we have a complete sentence or a significant chunk
            if any(p in buffer for p in ".!?") or len(buffer) > 512:
                audio = await text_to_speech(buffer)
                if audio:
                    audio_queue.put(audio)
                else:
                    audio_queue.put("skip")
                buffer = ""

    # Process any remaining text
    if buffer:
        audio = await text_to_speech(buffer)
        if audio:
            audio_queue.put(audio)
        else:
            audio_queue.put("skip")

    # Signal the end of the queue
    audio_queue.put(None)

async def main():
    print("Generating and speaking response...")
    
    # Start the audio playback thread
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()

    # Start streaming and speaking
    await stream_and_speak()

    # Wait for all audio to finish playing
    audio_queue.join()
    audio_thread.join()

    print("\nGeneration and playback complete.")

if __name__ == "__main__":
    asyncio.run(main())
