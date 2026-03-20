"""Microphone capture module."""
import tempfile
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000
CHANNELS = 1


class AudioCapture:
    """Captures microphone audio into a WAV file.

    Args:
        device: Sounddevice device index to use. None = system default.
    """

    def __init__(self, device: int | None = None) -> None:
        self._recording: list[np.ndarray] = []
        self._is_recording = False
        self._stream: sd.InputStream | None = None
        self._device = device

    def set_device(self, device: int | None) -> None:
        """Update the mic device. Takes effect on next start()."""
        self._device = device

    def start(self) -> None:
        """Start buffering audio from mic."""
        self._recording = []
        self._is_recording = True
        self._stream = self._make_stream()
        self._stream.start()

    def stop(self) -> Path:
        """Stop buffering and save to temp WAV file."""
        self._is_recording = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        audio = (
            np.concatenate(self._recording, axis=0)
            if self._recording
            else np.zeros((160, 1), dtype="float32")
        )
        return self._save_wav(audio)

    def feed(self, indata: np.ndarray) -> None:
        """Receive audio chunk from stream callback."""
        if self._is_recording:
            self._recording.append(indata.copy())

    def _make_stream(self) -> sd.InputStream:
        """Create a sounddevice input stream for the selected device."""
        return sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            device=self._device,
            callback=lambda indata, frames, time, status: self.feed(indata),
        )

    def _save_wav(self, audio: np.ndarray) -> Path:
        """Save numpy audio array to a temp WAV file."""
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        with wave.open(tmp.name, "wb") as wav:
            wav.setnchannels(CHANNELS)
            wav.setsampwidth(2)
            wav.setframerate(SAMPLE_RATE)
            wav.writeframes((audio * 32767).astype(np.int16).tobytes())
        return Path(tmp.name)


def list_microphones() -> list[dict]:
    """Return all available input devices.

    Returns:
        List of dicts with keys: index, name, channels.
    """
    devices = sd.query_devices()
    return [
        {
            "index": i,
            "name": d["name"],
            "channels": d["max_input_channels"],
        }
        for i, d in enumerate(devices)
        if d["max_input_channels"] > 0
    ]
