import os
import streamlit as st
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
            st.write(chunk_message)
            buffer += chunk_message
            if len(buffer) >= 128 or any(p in buffer for p in ".!?"):
                text_to_speech_and_play(buffer)
                buffer = ""
        time.sleep(0.01)  # Small delay to allow for speech to catch up

    # Process any remaining text
    if buffer:
        text_to_speech_and_play(buffer)

def main():
    st.title("OpenAI Chat with Text-to-Speech")
    st.write("Enter your message below and hear the response:")

    user_input = st.text_input("Your message:", "คุณเป็นใคร ทำอะไรได้บ้าง")

    if st.button("Submit"):
        stream = client.chat.completions.create(
            model="typhoon-v1.5x-70b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            max_tokens=512,
            temperature=0.6,
            top_p=0.95,
            stream=True,
        )

        # Start processing in a separate thread
        threading.Thread(target=wait_and_process_chunks, args=(stream,)).start()

        st.write(stream)
        st.write(text)

if __name__ == "__main__":
    main()
