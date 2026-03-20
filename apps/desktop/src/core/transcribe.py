"""Groq Whisper transcription module."""
from pathlib import Path

from groq import Groq

from ..config import get_settings


def transcribe(audio_path: Path) -> str:
    """Transcribe audio file using Groq Whisper Large v3 Turbo.
    
    Args:
        audio_path: Path to the WAV file to transcribe.
        
    Returns:
        Raw transcript text from Whisper.
    """
    settings = get_settings()
    client = Groq(api_key=settings.groq_api_key)

    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=f,
            language=None if settings.language == "auto" else settings.language,
        )

    # Clean up temp file after transcription
    audio_path.unlink(missing_ok=True)

    return result.text