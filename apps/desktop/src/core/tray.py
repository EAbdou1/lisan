"""System tray icon and menu for Lisan."""
import threading
from collections.abc import Callable

from PIL import Image, ImageDraw
import pystray


def _make_icon() -> Image.Image:
    """Draw a simple mic-shaped tray icon (32x32)."""
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Body of mic
    draw.rounded_rectangle([10, 2, 22, 20], radius=6, fill="#6366F1")
    # Stand
    draw.rectangle([15, 20, 17, 26], fill="#6366F1")
    # Base
    draw.ellipse([10, 25, 22, 29], fill="#6366F1")
    return img


class TrayIcon:
    """System tray icon with quick-access menu.

    Args:
        on_open: Called when user clicks Open.
        on_settings: Called when user clicks Settings.
        on_quit: Called when user clicks Quit.
    """

    def __init__(
        self,
        on_open: Callable[[], None],
        on_settings: Callable[[], None],
        on_quit: Callable[[], None],
    ) -> None:
        self._on_open = on_open
        self._on_settings = on_settings
        self._on_quit = on_quit
        self._icon: pystray.Icon | None = None

    def start(self) -> None:
        """Start the tray icon in a background thread."""
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self) -> None:
        """Remove the tray icon."""
        if self._icon:
            self._icon.stop()

    def set_status(self, status: str) -> None:
        """Update the tray tooltip to reflect current app status.

        Args:
            status: One of 'idle', 'recording', 'transcribing', 'cleaning', 'error'.
        """
        labels = {
            "idle": "Lisan — idle",
            "recording": "Lisan — recording...",
            "transcribing": "Lisan — transcribing...",
            "cleaning": "Lisan — cleaning...",
            "error": "Lisan — error",
        }
        if self._icon:
            self._icon.title = labels.get(status, "Lisan")

    def _run(self) -> None:
        menu = pystray.Menu(
            pystray.MenuItem("Open Lisan", self._handle_open, default=True),
            pystray.MenuItem("Settings", self._handle_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._handle_quit),
        )
        self._icon = pystray.Icon(
            name="lisan",
            icon=_make_icon(),
            title="Lisan — idle",
            menu=menu,
        )
        self._icon.run()

    def _handle_open(self) -> None:
        self._on_open()

    def _handle_settings(self) -> None:
        self._on_settings()

    def _handle_quit(self) -> None:
        self.stop()
        self._on_quit()
