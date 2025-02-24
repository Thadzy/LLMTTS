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
os.environ["OPENAI_API_KEY"] = "sk-JoABD96Rui1GWSrpJ6h78lTDEkbQG386TWBYZWLPQHoWewkU"
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.opentyphoon.ai/v1",
)

async def get_response_and_tokenize():
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

    response_text = ""
    tokenizer = Tokenizer()

    # Collect and tokenize the response as it streams
    async for chunk in stream:
        if "choices" in chunk:
            chunk_text = chunk["choices"][0]["delta"].get("content", "")
            response_text += chunk_text
            print(f"Received chunk: {chunk_text}")

            # Tokenize the current chunk
            tokens = tokenizer.split(chunk_text)
            print(f"Tokens: {tokens}")

    print("\nFinal Response:")
    print(response_text)
    return response_text

async def main():
    await get_response_and_tokenize()

if __name__ == "__main__":
    asyncio.run(main())
