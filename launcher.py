#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""
ViralMint Launcher — Toolbox for non-technical users.
Double-click to open. System tray icon + optional GUI window.

Features:
  - System tray with the real ViralMint icon + green/red status badge
  - Tray menu: Start/Stop Service, Open WebUI, Show Launcher, Quit
  - If tkinter available: a dark-themed launcher window with buttons
  - Close window → minimizes to tray (service keeps running)
  - Quit from tray → stops everything and exits
"""
import sys
import os
import subprocess
import threading
import webbrowser
import time
import platform
from pathlib import Path

# ─── Constants ─────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
PORT = 16888
URL = f"http://localhost:{PORT}"
APP_NAME = "ViralMint"
ICON_PATH = ROOT / "frontend" / "public" / "icon-192.png"

# ─── Backend process management ────────────────────────────────────────────────

_backend_process = None
_status_lock = threading.Lock()


def _find_python():
    """Find the best Python executable (venv preferred)."""
    venv_dir = "Scripts" if platform.system() == "Windows" else "bin"
    for name in ("python3", "python"):
        p = ROOT / "venv" / venv_dir / name
        if p.exists():
            return str(p)
    return sys.executable


def is_running():
    """Check if the backend process is alive."""
    with _status_lock:
        return _backend_process is not None and _backend_process.poll() is None


def start_service():
    """Start the ViralMint backend server."""
    global _backend_process
    with _status_lock:
        if _backend_process and _backend_process.poll() is None:
            return True

    env = os.environ.copy()
    env["PORT"] = str(PORT)

    try:
        kwargs = {}
        if platform.system() == "Windows":
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            kwargs["startupinfo"] = info

        _backend_process = subprocess.Popen(
            [_find_python(), str(ROOT / "run.py")],
            cwd=str(ROOT),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            **kwargs,
        )
        return True
    except Exception as e:
        print(f"Failed to start service: {e}")
        return False


def stop_service():
    """Stop the ViralMint backend server."""
    global _backend_process
    with _status_lock:
        if _backend_process is None:
            return
        try:
            _backend_process.terminate()
            _backend_process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            _backend_process.kill()
        except Exception:
            pass
        _backend_process = None


def open_webui():
    """Open the WebUI in the default browser."""
    webbrowser.open(URL)


def wait_for_server(timeout=30):
    """Block until the server is ready or timeout."""
    import urllib.request
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(URL, timeout=2)
            return True
        except Exception:
            time.sleep(0.5)
    return False


# ─── Tray Icon Rendering ──────────────────────────────────────────────────────

def _make_tray_icon(running: bool):
    """
    Build tray icon: the real ViralMint logo resized to 64x64
    with a small colored status badge in the bottom-right corner.
      - Green badge  = service running
      - Gray badge   = service stopped
    """
    from PIL import Image, ImageDraw

    size = 64
    badge_r = 10  # badge radius

    # Load and resize the real app icon
    if ICON_PATH.exists():
        try:
            base = Image.open(ICON_PATH).convert("RGBA").resize((size, size), Image.LANCZOS)
        except Exception:
            base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    else:
        base = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    draw = ImageDraw.Draw(base)

    # Badge position: bottom-right corner
    bx = size - badge_r * 2 - 2
    by = size - badge_r * 2 - 2

    # White ring (border) behind the badge for contrast
    ring_pad = 3
    draw.ellipse(
        [bx - ring_pad, by - ring_pad, bx + badge_r * 2 + ring_pad, by + badge_r * 2 + ring_pad],
        fill=(255, 255, 255, 230),
    )

    # Status badge
    badge_color = (16, 185, 129, 255) if running else (156, 163, 175, 255)
    draw.ellipse([bx, by, bx + badge_r * 2, by + badge_r * 2], fill=badge_color)

    return base


# ─── System Tray (pystray) ────────────────────────────────────────────────────

_tray_icon = None
_gui_callback = None  # set by GUI if tkinter is available


def _refresh_tray():
    """Update tray icon + rebuild menu to reflect current state."""
    if _tray_icon:
        _tray_icon.icon = _make_tray_icon(is_running())
        _tray_icon.update_menu()


def _tray_start(icon, item):
    if is_running():
        return
    start_service()
    _refresh_tray()
    if _gui_callback:
        _gui_callback("starting")

    def _wait():
        ready = wait_for_server(30)
        _refresh_tray()
        if _gui_callback:
            _gui_callback("ready" if ready else "failed")

    threading.Thread(target=_wait, daemon=True).start()


def _tray_stop(icon, item):
    if not is_running():
        return
    stop_service()
    _refresh_tray()
    if _gui_callback:
        _gui_callback("stopped")


def _tray_open(icon, item):
    if is_running():
        open_webui()


def _tray_show(icon, item):
    if _gui_callback:
        _gui_callback("show")


def _tray_quit(icon, item):
    stop_service()
    icon.stop()
    if _gui_callback:
        _gui_callback("quit")


def create_tray():
    """Create the system tray icon (call .run() to start it)."""
    global _tray_icon
    import pystray
    from pystray import MenuItem as Item

    def _menu():
        running = is_running()
        items = [
            Item(
                "Start Service" if not running else "Service Running",
                _tray_start,
                enabled=not running,
            ),
            Item("Stop Service", _tray_stop, enabled=running),
            pystray.Menu.SEPARATOR,
            Item("Open WebUI", _tray_open, enabled=running, default=True),
        ]
        if _gui_callback:
            items.append(pystray.Menu.SEPARATOR)
            items.append(Item("Show Launcher", _tray_show))
        items.append(pystray.Menu.SEPARATOR)
        items.append(Item("Quit ViralMint", _tray_quit))
        return pystray.Menu(*items)

    _tray_icon = pystray.Icon(
        APP_NAME,
        _make_tray_icon(False),
        f"{APP_NAME} — Stopped",
        menu=_menu(),
    )
    return _tray_icon


def _update_tray_title():
    """Keep the tray tooltip text in sync with status."""
    if _tray_icon:
        if is_running():
            _tray_icon.title = f"{APP_NAME} — Running (port {PORT})"
        else:
            _tray_icon.title = f"{APP_NAME} — Stopped"


# ─── GUI Window (tkinter — optional) ──────────────────────────────────────────

def _run_with_gui():
    """Launch with tkinter window + system tray."""
    import tkinter as tk
    from tkinter import font as tkfont

    root = tk.Tk()
    root.title(f"{APP_NAME} Launcher")
    root.resizable(False, False)

    win_w, win_h = 400, 360
    sx, sy = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{win_w}x{win_h}+{(sx - win_w) // 2}+{(sy - win_h) // 3}")

    # ── Theme ──
    BG       = "#0f172a"
    BG_CARD  = "#1e293b"
    BORDER   = "#334155"
    GREEN    = "#10b981"
    RED      = "#ef4444"
    BLUE     = "#3b82f6"
    GRAY     = "#64748b"
    TEXT     = "#f1f5f9"
    TEXT_DIM = "#94a3b8"

    root.configure(bg=BG)

    # Window icon
    if ICON_PATH.exists():
        try:
            _tk_icon = tk.PhotoImage(file=str(ICON_PATH))
            root.iconphoto(True, _tk_icon)
        except Exception:
            pass

    # Fonts
    title_font = tkfont.Font(family="Helvetica Neue", size=20, weight="bold")
    status_font = tkfont.Font(family="Helvetica Neue", size=11)
    btn_font = tkfont.Font(family="Helvetica Neue", size=13, weight="bold")
    foot_font = tkfont.Font(family="Helvetica Neue", size=9)

    # ── Header ──
    hdr = tk.Frame(root, bg=BG)
    hdr.pack(fill="x", padx=32, pady=(28, 0))
    tk.Label(hdr, text=APP_NAME, font=title_font, fg=GREEN, bg=BG).pack(side="left")
    # Version badge
    ver = tk.Label(hdr, text="v1.0", font=foot_font, fg=GRAY, bg=BG)
    ver.pack(side="left", padx=(8, 0), pady=(6, 0))

    # ── Status bar ──
    sf = tk.Frame(root, bg=BG)
    sf.pack(fill="x", padx=32, pady=(14, 0))

    dot_cv = tk.Canvas(sf, width=14, height=14, bg=BG, highlightthickness=0)
    dot_cv.pack(side="left", padx=(0, 8))
    dot_id = dot_cv.create_oval(2, 2, 12, 12, fill=GRAY, outline="")

    status_lbl = tk.Label(sf, text="Service stopped", font=status_font, fg=TEXT_DIM, bg=BG)
    status_lbl.pack(side="left")

    # ── Card ──
    card = tk.Frame(root, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
    card.pack(fill="x", padx=32, pady=(22, 0))
    inner = tk.Frame(card, bg=BG_CARD)
    inner.pack(padx=22, pady=22, fill="x")

    # ── UI update helper ──
    def set_ui(state):
        """state: 'running' | 'stopped' | 'starting' | 'failed'"""
        if state == "running":
            dot_cv.itemconfig(dot_id, fill=GREEN)
            status_lbl.config(text=f"Service running on port {PORT}", fg=GREEN)
            ss_btn.config(text="Stop Service", bg=RED, activebackground="#dc2626", state="normal")
            web_btn.config(state="normal", bg=BLUE, fg=TEXT)
        elif state == "stopped":
            dot_cv.itemconfig(dot_id, fill=GRAY)
            status_lbl.config(text="Service stopped", fg=TEXT_DIM)
            ss_btn.config(text="Start Service", bg=GREEN, activebackground="#059669", state="normal")
            web_btn.config(state="disabled", bg="#374151", fg=GRAY)
        elif state == "starting":
            dot_cv.itemconfig(dot_id, fill="#facc15")  # yellow
            status_lbl.config(text="Starting service...", fg="#facc15")
            ss_btn.config(text="Starting...", state="disabled")
        elif state == "failed":
            dot_cv.itemconfig(dot_id, fill=RED)
            status_lbl.config(text="Failed to start service", fg=RED)
            ss_btn.config(text="Start Service", bg=GREEN, activebackground="#059669", state="normal")
        _update_tray_title()

    # ── Button handlers ──
    def on_toggle():
        if is_running():
            set_ui("starting")
            root.update()
            stop_service()
            set_ui("stopped")
            _refresh_tray()
        else:
            set_ui("starting")
            root.update()
            ok = start_service()
            if ok:
                def _wait():
                    ready = wait_for_server(30)
                    root.after(0, lambda: _finish_start(ready))
                threading.Thread(target=_wait, daemon=True).start()
            else:
                set_ui("failed")

    def _finish_start(ready):
        set_ui("running" if ready else "failed")
        _refresh_tray()

    # ── Start/Stop button ──
    ss_btn = tk.Button(
        inner, text="Start Service", font=btn_font,
        bg=GREEN, fg=TEXT, activebackground="#059669", activeforeground=TEXT,
        relief="flat", cursor="hand2", bd=0, pady=12,
        command=on_toggle,
    )
    ss_btn.pack(fill="x", pady=(0, 12))

    # ── Open WebUI button ──
    web_btn = tk.Button(
        inner, text="Open WebUI", font=btn_font,
        bg="#374151", fg=GRAY, activebackground="#2563eb", activeforeground=TEXT,
        relief="flat", cursor="hand2", bd=0, pady=12, state="disabled",
        command=lambda: open_webui() if is_running() else None,
    )
    web_btn.pack(fill="x")

    # ── Footer ──
    tk.Label(
        root, text=f"{URL}  \u2022  Close window to minimize to tray",
        font=foot_font, fg=TEXT_DIM, bg=BG,
    ).pack(side="bottom", pady=(0, 16))

    # ── Wire tray ↔ GUI ──
    global _gui_callback

    def gui_cb(event):
        if event == "quit":
            root.after(0, root.destroy)
        elif event == "show":
            root.after(0, root.deiconify)
        elif event == "starting":
            root.after(0, lambda: set_ui("starting"))
        elif event == "ready":
            root.after(0, lambda: set_ui("running"))
        elif event == "stopped":
            root.after(0, lambda: set_ui("stopped"))
        elif event == "failed":
            root.after(0, lambda: set_ui("failed"))

    _gui_callback = gui_cb

    # Start tray
    tray = create_tray()
    threading.Thread(target=tray.run, daemon=True).start()

    # ── Window close → minimize to tray ──
    def on_close():
        if is_running():
            root.withdraw()
        else:
            stop_service()
            if _tray_icon:
                _tray_icon.stop()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

    # Final cleanup
    stop_service()
    if _tray_icon:
        try:
            _tray_icon.stop()
        except Exception:
            pass


# ─── Tray-only fallback ───────────────────────────────────────────────────────

def _run_tray_only():
    """System tray only — when tkinter is not available."""
    print(f"\n  {APP_NAME} Launcher (tray mode)")
    print(f"  Right-click the tray icon to control the service.")
    print(f"  Service URL: {URL}\n")

    tray = create_tray()
    tray.run()  # blocks until Quit
    stop_service()


# ─── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.chdir(ROOT)

    try:
        import tkinter  # noqa: F401
        _run_with_gui()
    except ImportError:
        print("Note: tkinter not available, using tray-only mode")
        _run_tray_only()
