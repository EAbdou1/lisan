"""Pywebview JS <-> Python bridge."""
import json
import threading
import time

from core.audio import AudioCapture, list_microphones
from core.cleanup import clean
from core.hotkey import HotkeyListener
from core.inject import inject
from core.transcribe import transcribe
from core.tray import TrayIcon
from config import get_settings, save_runtime_settings
from db.local import (
    delete_snippet as db_delete_snippet,
    get_history as db_get_history,
    get_snippets as db_get_snippets,
    init_db,
    save_history,
    save_snippet as db_save_snippet,
)


class LisanBridge:
    """All public methods are callable from React via window.pywebview.api.

    Args:
        mini: The mini pywebview window instance.
        dashboard: The dashboard pywebview window instance.
    """

    def __init__(self, mini: object, dashboard: object) -> None:
        self._mini = mini
        self._dashboard = dashboard
        self._tray: TrayIcon | None = None
        settings = get_settings()
        self._audio = AudioCapture(device=settings.mic_device)
        self._start_time: float = 0
        self._hotkey_listener: HotkeyListener | None = None
        self._hide_timer: threading.Timer | None = None
        init_db()
        self._start_hotkey_listener()

    # ── Internal ────────────────────────────────────────────────

    def set_tray(self, tray: TrayIcon) -> None:
        """Inject tray reference after construction."""
        self._tray = tray

    def _notify(self, event: str, data: object) -> None:
        """Push event to both windows."""
        payload = json.dumps(data)
        js = f"window.lisanEvent('{event}', {payload})"
        self._mini.evaluate_js(js)        # type: ignore
        self._dashboard.evaluate_js(js)   # type: ignore
        if event == "status" and self._tray:
            self._tray.set_status(str(data))

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
        """Show mini window and start recording."""
        # Cancel any pending hide
        if self._hide_timer:
            self._hide_timer.cancel()
            self._hide_timer = None

        self._mini.show()                  # type: ignore
        self._audio.start()
        self._start_time = time.time()
        self._notify("status", "recording")

    def stop_recording(self) -> None:
        """Stop mic capture and kick off processing. Called on hotkey release."""
        duration = int(time.time() - self._start_time)
        self._notify("status", "transcribing")
        threading.Thread(
            target=self._process,
            args=(duration,),
            daemon=True,
        ).start()

    def _process(self, duration: int) -> None:
        """Full pipeline: audio → Whisper → Llama → inject → hide after 5s."""
        try:
            audio_path = self._audio.stop()

            raw = transcribe(audio_path)

            self._notify("status", "cleaning")
            cleaned = clean(raw) or raw

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

            # Hide mini window after 5 seconds
            self._hide_timer = threading.Timer(5.0, self._hide_mini)
            self._hide_timer.start()

        except Exception as e:  # noqa: BLE001
            self._notify("error", str(e))
            self._notify("status", "idle")
            self._hide_timer = threading.Timer(5.0, self._hide_mini)
            self._hide_timer.start()

    def _hide_mini(self) -> None:
        """Hide the mini window and reset timer."""
        self._mini.hide()                  # type: ignore
        self._hide_timer = None

    # ── History ─────────────────────────────────────────────────

    def get_history(self) -> list[dict]:
        """Return last 50 transcriptions."""
        return db_get_history()

    # ── Snippets ────────────────────────────────────────────────

    def get_snippets(self) -> list[dict]:
        """Return all saved snippets."""
        return db_get_snippets()

    def save_snippet(self, trigger: str, expansion: str) -> None:
        """Save or update a snippet."""
        db_save_snippet(trigger, expansion)

    def delete_snippet(self, snippet_id: int) -> None:
        """Delete a snippet by ID."""
        db_delete_snippet(snippet_id)

    # ── Settings ────────────────────────────────────────────────

    def get_settings(self) -> dict:
        """Return current app settings including available mics."""
        s = get_settings()
        return {
            "hotkey": s.hotkey,
            "language": s.language,
            "cleanupMode": s.cleanup_mode,
            "micDevice": s.mic_device,
            "microphones": list_microphones(),
        }

    def save_settings(
        self,
        hotkey: str | None = None,
        language: str | None = None,
        cleanup_mode: str | None = None,
        mic_device: int | None = None,
    ) -> None:
        """Persist new settings and apply them immediately.

        Args:
            hotkey: New hotkey string e.g. 'alt+space'.
            language: Transcription language e.g. 'ar', 'en', 'auto'.
            cleanup_mode: One of 'light', 'aggressive', 'off'.
            mic_device: Sounddevice device index, or None for system default.
        """
        updates: dict = {}

        if hotkey is not None:
            updates["hotkey"] = hotkey
            if self._hotkey_listener:
                self._hotkey_listener.restart(hotkey)

        if language is not None:
            updates["language"] = language

        if cleanup_mode is not None:
            updates["cleanup_mode"] = cleanup_mode

        if mic_device is not None:
            updates["mic_device"] = mic_device
            self._audio.set_device(mic_device)

        if updates:
            save_runtime_settings(updates)

        self._notify("status", "idle")

    def get_microphones(self) -> list[dict]:
        """Return all available input devices."""
        return list_microphones()
