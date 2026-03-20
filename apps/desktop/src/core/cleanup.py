"""Groq LLM transcript cleanup module."""
from groq import Groq

from ..config import get_settings

SYSTEM_PROMPT = """You are a dictation cleanup assistant.
Your job:
- Remove filler words (um, uh, like, you know, so, basically)
- Fix grammar and punctuation
- Keep the meaning exactly as intended
- Return ONLY the cleaned text, nothing else
- Preserve Arabic text as-is, only clean fillers"""


def clean(raw: str) -> str:
    """Clean up raw Whisper transcript using Groq Llama.

    Args:
        raw: Raw transcript text from Whisper.

    Returns:
        Cleaned and polished transcript text.
    """
    settings = get_settings()
    client = Groq(api_key=settings.groq_api_key)

    result = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=500,
        temperature=0.1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw},
        ],
    )

    return result.choices[0].message.content.strip()