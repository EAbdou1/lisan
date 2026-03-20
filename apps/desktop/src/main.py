"""Lisan desktop app entry point."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import webview
from api.bridge import LisanBridge
from core.tray import TrayIcon


def main() -> None:
    """Create and launch the pywebview window."""
    window = webview.create_window(
        title="LISAN",
        url="http://localhost:5173",  # Vite dev server
        width=200,
        height=200,
        resizable=False,
        frameless=True,
        on_top=True,
        transparent=True,
        background_color="#000000",
    )

    bridge = LisanBridge(window)

    # Expose all bridge methods to React
    window.expose(bridge.start_recording)
    window.expose(bridge.stop_recording)
    window.expose(bridge.get_history)
    window.expose(bridge.get_snippets)
    window.expose(bridge.save_snippet)
    window.expose(bridge.delete_snippet)
    window.expose(bridge.get_settings)
    window.expose(bridge.save_settings)

    tray = TrayIcon(
        on_open=lambda: window.show(),
        on_settings=lambda: window.evaluate_js(
            "window.lisanEvent('navigate', 'settings')"
        ),
        on_quit=lambda: window.destroy(),
    )
    bridge._tray = tray
    tray.start()

    webview.start(debug=True)


if __name__ == "__main__":
    main()