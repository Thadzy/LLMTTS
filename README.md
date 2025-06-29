Here is the revised `README.md` for your **LLMTTS** project, strictly professional and without emojis:

---

# LLMTTS (Large Language Model Text-to-Speech)

**LLMTTS** is a Python-based real-time system that streams responses from a Large Language Model (LLM) and converts them into speech using Microsoft Edge TTS and `pygame`. It supports Thai and English, streaming text generation, dynamic audio buffering, and voice fallback.

---

## Features

* Real-time text generation and audio playback
* Seamless voice fallback mechanism across multiple TTS voices
* Thai language support with optional tokenization
* Text-to-speech conversion using Microsoft Edge neural voices
* Integration with OpenTyphoon LLM via OpenAI-compatible API

---

## How It Works

1. Sends a user prompt to the OpenTyphoon LLM.
2. Streams generated text token by token.
3. Buffers text until a sentence is complete or a threshold is reached.
4. Converts buffered text to audio using `edge-tts`.
5. Plays audio in real-time using `pygame` while streaming continues.

---

## Requirements

Install the dependencies with:

```bash
pip install openai edge-tts pygame thai-tokenizer
```

Additional system requirement: `ffmpeg` must be installed and available in your system path for `edge-tts` to function.

---

## Environment Setup

Set the environment variable for your API key:

```python
os.environ["OPENAI_API_KEY"] = "<your-api-key>"
```

Make sure to point to the correct base URL if using a custom or third-party LLM service:

```python
base_url="https://api.opentyphoon.ai/v1"
```

---

## Voice Support

The system uses the following Microsoft neural voices (in priority order):

* `th-TH-NiwatNeural`
* `th-TH-PremwadeeNeural`
* `en-US-ChristopherNeural`

It will attempt fallback in this order if a voice fails during audio generation.

---

## Directory Structure

```
LLMTTS/
├── llmtts.py             # Main application script
├── requirements.txt      # Optional, list of dependencies
└── README.md             # Documentation
```

---

## Usage Example

```python
messages = [
    {
        "role": "user",
        "content": "วันนี้กินข้าวกับอะไรดี"
    }
]
```

The model responds in real-time, and the audio is generated and played sentence-by-sentence.

---

## Notes

* The `Tokenizer` from `thai_tokenizer` is initialized for future use in sentence segmentation or domain-specific parsing.
* The queue-based design ensures audio playback does not block streaming or processing.
* This script is suitable for voice assistants, chatbots, or language learning tools.

---
