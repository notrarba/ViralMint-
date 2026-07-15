#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2025-2026 ViralMint Contributors
"""Packaged desktop entry point.

Used when ViralMint is run from a PyInstaller-built .app/.exe bundle. For dev
runs from a source checkout, use `python run.py` instead — that one builds
the frontend, installs npm deps, etc.

Layout assumptions in frozen mode:
  - sys._MEIPASS is the unpacked bundle root (read-only on macOS).
  - The frontend SPA lives at sys._MEIPASS/frontend/dist (bundled at build
    time). We pass that path to backend/main.py via VIRALMINT_FRONTEND_DIST.
  - User-writable state — SQLite DB, encrypted credentials, downloaded
    videos, generated output, logs — lives at VIRALMINT_DATA_DIR
    (defaults to ~/ViralMint). We chdir there before importing the backend
    so SQLite's "./viralmint.db", storage/, and .env all resolve under it.
"""
from __future__ import annotations

import logging
import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path


def _resolve_data_dir() -> Path:
    data_dir = Path(os.environ.get("VIRALMINT_DATA_DIR", Path.home() / "ViralMint"))
    data_dir.mkdir(parents=True, exist_ok=True)
    for sub in (
        "storage/videos", "storage/audio", "storage/generated",
        "storage/thumbnails", "storage/tmp", "logs",
    ):
        (data_dir / sub).mkdir(parents=True, exist_ok=True)
    return data_dir


def _resolve_frontend_dist() -> Path | None:
    if env := os.environ.get("VIRALMINT_FRONTEND_DIST"):
        p = Path(env)
        return p if p.exists() else None
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    candidate = bundle_root / "frontend" / "dist"
    return candidate if candidate.exists() else None


def _wait_for_port_then_open_browser(host: str, port: int, timeout: float = 30.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                webbrowser.open(f"http://{host}:{port}")
                return
        except OSError:
            time.sleep(0.3)
    logging.getLogger("viralmint.app").warning(
        "Server did not become ready in %.0fs — not opening browser.", timeout
    )


def main() -> None:
    # Defense in depth: in a frozen PyInstaller bundle, sys.executable points
    # at this binary itself. Any code that does `subprocess.run([sys.executable,
    # "-m", ...])` would re-invoke desktop_app.main() and fork-bomb. Refuse to
    # run if argv looks like a Python module-runner invocation rather than a
    # direct user launch — exit cleanly so the parent's subprocess.run() gets
    # a non-zero return instead of spawning another whole launcher.
    if any(arg in ("-m", "-c") for arg in sys.argv[1:]) or any(
        arg.startswith("-") and arg != "--" for arg in sys.argv[1:]
    ):
        sys.stderr.write(
            f"ViralMint launcher invoked with module-runner args {sys.argv[1:]!r}; "
            "this happens when packaged code calls subprocess.run([sys.executable, ...]).\n"
            "Refusing to recurse — fix the caller.\n"
        )
        sys.exit(2)

    data_dir = _resolve_data_dir()
    os.chdir(data_dir)

    if (fe := _resolve_frontend_dist()) is not None:
        os.environ.setdefault("VIRALMINT_FRONTEND_DIST", str(fe))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(data_dir / "logs" / "app.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    log = logging.getLogger("viralmint.app")
    log.info("Starting ViralMint — data_dir=%s", data_dir)
    log.info("Frontend dist: %s", os.environ.get("VIRALMINT_FRONTEND_DIST", "<none>"))

    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "16888"))

    threading.Thread(
        target=_wait_for_port_then_open_browser,
        args=(host, port),
        daemon=True,
    ).start()

    import uvicorn
    from backend.main import app  # noqa: E402

    uvicorn.run(app, host=host, port=port, log_level="info", access_log=False)


if __name__ == "__main__":
    main()
