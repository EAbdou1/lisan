"""Pywebview JS <-> Python bridge."""
import json
import threading
import time

import sounddevice as sd

from ..core.audio import AudioCapture
from ..core.cleanup import clean
from ..core.hotkey import HotkeyListener
from ..core.inject import inject
from ..core.transcribe import transcribe
from ..config import get_settings
from ..db.local import (
    delete_snippet,
    get_history,
    get_snippets,
    init_db,
    save_history,
    save_snippet,
)


class LisanBridge:
    """All public methods are callable from React via window.pywebview.api.

    Args:
        window: The pywebview window instance.
    """

    def __init__(self, window: object) -> None:
        self._window = window
        self._audio = AudioCapture()
        self._stream: sd.InputStream | None = None
        self._start_time: float = 0
        self._hotkey_listener: HotkeyListener | None = None
        init_db()
        self._start_hotkey_listener()

    # ── Internal ────────────────────────────────────────────────

    def _notify(self, event: str, data: object) -> None:
        """Push an event to React via JS evaluation."""
        payload = json.dumps(data)
        self._window.evaluate_js(  # type: ignore
            f"window.lisanEvent('{event}', {payload})"
        )

    def _start_hotkey_listener(self) -> None:
        """Start listening for the global hotkey."""
        settings = get_settings()
        self._hotkey_listener = HotkeyListener(
            hotkey=settings.hotkey,
            on_press=self.start_recording,
            on_release=self.stop_recording,
        )
        self._hotkey_listener.start()

    # ── Recording ───────────────────────────────────────────────

    def start_recording(self) -> None:
        """Start mic capture. Called on hotkey press."""
        self._audio.start()
        self._start_time = time.time()
        self._stream = self._audio.get_stream()
        self._stream.start()
        self._notify("status", "recording")

    def stop_recording(self) -> None:
        """Stop mic capture and kick off processing. Called on hotkey release."""
        if self._stream:
            self._stream.stop()
            self._stream.close()

        duration = int(time.time() - self._start_time)
        self._notify("status", "transcribing")

        threading.Thread(
            target=self._process,
            args=(duration,),
            daemon=True,
        ).start()

    def _process(self, duration: int) -> None:
        """Full pipeline: audio → Whisper → Llama → inject."""
        try:
            audio_path = self._audio.stop()

            raw = transcribe(audio_path)

            self._notify("status", "cleaning")
            cleaned = clean(raw)

            word_count = len(cleaned.split())

            save_history(
                raw=raw,
                cleaned=cleaned,
                word_count=word_count,
                duration=duration,
            )

            inject(cleaned)

            self._notify("transcript", {
                "raw": raw,
                "cleaned": cleaned,
                "wordCount": word_count,
                "duration": duration,
            })
            self._notify("status", "idle")

        except Exception as e:  # noqa: BLE001
            self._notify("error", str(e))
            self._notify("status", "idle")

    # ── History ─────────────────────────────────────────────────

    def get_history(self) -> list[dict]:
        """Return last 50 transcriptions."""
        return get_history()

    # ── Snippets ────────────────────────────────────────────────

    def get_snippets(self) -> list[dict]:
        """Return all saved snippets."""
        return get_snippets()

    def save_snippet(self, trigger: str, expansion: str) -> None:
        """Save or update a snippet."""
        save_snippet(trigger, expansion)

    def delete_snippet(self, snippet_id: int) -> None:
        """Delete a snippet by ID."""
        delete_snippet(snippet_id)

    # ── Settings ────────────────────────────────────────────────

    def get_settings(self) -> dict:
        """Return current app settings."""
        s = get_settings()
        return {
            "hotkey": s.hotkey,
            "language": s.language,
            "cleanupMode": s.cleanup_mode,
        }