"""Global hotkey listener module."""
from collections.abc import Callable

import keyboard


class HotkeyListener:
    """Listens for a global hotkey combination system-wide.

    Works even when the app window is not focused.

    Args:
        hotkey: Key combination string e.g. 'alt+space'.
        on_press: Callback fired when hotkey is pressed.
        on_release: Callback fired when hotkey is released.
    """

    def __init__(
        self,
        hotkey: str,
        on_press: Callable[[], None],
        on_release: Callable[[], None],
    ) -> None:
        self._hotkey = hotkey
        self._on_press = on_press
        self._on_release = on_release
        self._pressed = False
        self._parse_hotkey(hotkey)

    def _parse_hotkey(self, hotkey: str) -> None:
        """Extract modifier and key from a hotkey string like 'alt+space'."""
        parts = hotkey.split("+")
        self._modifier = parts[0]
        self._key = parts[-1]

    def start(self) -> None:
        """Start listening for the hotkey."""
        keyboard.on_press_key(self._key, self._handle_press)
        keyboard.on_release_key(self._key, self._handle_release)

    def stop(self) -> None:
        """Stop listening and clean up all hooks."""
        keyboard.unhook_all()
        self._pressed = False

    def restart(self, new_hotkey: str) -> None:
        """Swap to a new hotkey combination without restarting the app.

        Args:
            new_hotkey: New key combination string e.g. 'ctrl+shift+space'.
        """
        self.stop()
        self._hotkey = new_hotkey
        self._parse_hotkey(new_hotkey)
        self.start()

    def _handle_press(self, _: object) -> None:
        if keyboard.is_pressed(self._modifier) and not self._pressed:
            self._pressed = True
            self._on_press()

    def _handle_release(self, _: object) -> None:
        if self._pressed:
            self._pressed = False
            self._on_release()
