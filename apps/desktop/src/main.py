"""Lisan desktop app entry point."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import webview
from api.bridge import LisanBridge
from core.tray import TrayIcon


def get_bottom_right(width: int, height: int) -> tuple[int, int]:
    """Calculate bottom-right screen position with 24px margin.

    Args:
        width: Window width in pixels.
        height: Window height in pixels.

    Returns:
        (x, y) position tuple.
    """
    screens = webview.screens
    screen = screens[0]
    x = screen.width - width - 24
    y = screen.height - height - 24
    return x, y


def main() -> None:
    """Create and launch both pywebview windows."""

    mini_w, mini_h = 320, 80
    dash_w, dash_h = 900, 600
    mini_x, mini_y = get_bottom_right(mini_w, mini_h)

    # Mini window — always on top, frameless, transparent
    mini = webview.create_window(
        title="Lisan",
        url="http://localhost:5173/?window=mini",
        width=mini_w,
        height=mini_h,
        x=mini_x,
        y=mini_y,
        resizable=False,
        frameless=True,
        on_top=True,
        transparent=True,
        background_color="#00000000",
        hidden=True,  # starts hidden, bridge shows it on hotkey press
    )

    # Dashboard window — normal, opens from tray
    dashboard = webview.create_window(
        title="Lisan — Dashboard",
        url="http://localhost:5173/?window=dashboard",
        width=dash_w,
        height=dash_h,
        resizable=True,
        frameless=False,
        on_top=False,
        hidden=True,  # starts hidden, tray shows it
    )

    bridge = LisanBridge(mini=mini, dashboard=dashboard)

    # Expose bridge to both windows
    for window in (mini, dashboard):
        window.expose(bridge.start_recording)
        window.expose(bridge.stop_recording)
        window.expose(bridge.get_history)
        window.expose(bridge.get_snippets)
        window.expose(bridge.save_snippet)
        window.expose(bridge.delete_snippet)
        window.expose(bridge.get_settings)
        window.expose(bridge.save_settings)

    tray = TrayIcon(
        on_open=lambda: dashboard.show(),
        on_settings=lambda: (
            dashboard.show(),
            dashboard.evaluate_js("window.lisanEvent('navigate','settings')"),
        ),
        on_quit=lambda: webview.exit(),
    )
    tray.start()
    bridge.set_tray(tray)

    webview.start(debug=True)


if __name__ == "__main__":
    main()
