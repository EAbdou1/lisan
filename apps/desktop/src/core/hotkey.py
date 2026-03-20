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

        parts = hotkey.split("+")
        self._modifier = parts[0]
        self._key = parts[-1]

    def start(self) -> None:
        """Start listening for the hotkey."""
        keyboard.on_press_key(self._key, self._handle_press)
        keyboard.on_release_key(self._key, self._handle_release)

    def stop(self) -> None:
        """Stop listening and clean up hooks."""
        keyboard.unhook_all()

    def _handle_press(self, _: object) -> None:
        if keyboard.is_pressed(self._modifier) and not self._pressed:
            self._pressed = True
            self._on_press()

    def _handle_release(self, _: object) -> None:
        if self._pressed:
            self._pressed = False
            self._on_release()