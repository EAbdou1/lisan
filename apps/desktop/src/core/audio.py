"""Microphone capture module."""
import tempfile
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000
CHANNELS = 1


class AudioCapture:
    def __init__(self) -> None:
        self._recording: list[np.ndarray] = []
        self._is_recording = False

    def start(self) -> None:
        """Start buffering audio from mic."""
        self._recording = []
        self._is_recording = True

    def stop(self) -> Path:
        """Stop buffering and save to temp wav file."""
        self._is_recording = False
        audio = np.concatenate(self._recording, axis=0)
        return self._save_wav(audio)

    def feed(self, indata: np.ndarray) -> None:
        """Receive audio chunk from stream callback."""
        if self._is_recording:
            self._recording.append(indata.copy())

    def get_stream(self) -> sd.InputStream:
        """Create a sounddevice input stream."""
        return sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            callback=lambda indata, frames, time, status: self.feed(indata),
        )

    def _save_wav(self, audio: np.ndarray) -> Path:
        """Save numpy audio array to a temp wav file."""
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        with wave.open(tmp.name, "wb") as wav:
            wav.setnchannels(CHANNELS)
            wav.setsampwidth(2)
            wav.setframerate(SAMPLE_RATE)
            wav.writeframes((audio * 32767).astype(np.int16).tobytes())
        return Path(tmp.name)