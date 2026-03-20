"""Text injection into the currently focused application."""
import platform
import time

import pyperclip
import pyautogui


def inject(text: str) -> None:
    """Inject text into whatever app currently has focus.

    Works by copying text to clipboard and simulating
    a paste keystroke in the active application.

    Args:
        text: The cleaned transcript to inject.
    """
    pyperclip.copy(text)
    time.sleep(0.15)  # let target app reclaim focus before paste

    system = platform.system()
    if system == "Darwin":  # Mac
        pyautogui.hotkey("command", "v")
    else:  # Windows + Linux
        pyautogui.hotkey("ctrl", "v")