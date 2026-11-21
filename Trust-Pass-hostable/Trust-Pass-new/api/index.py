"""Vercel request-based API function. Local use: python backend/server.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.server import Handler, init_db

_ready = False


class handler(Handler):
    """Vercel's Python runtime looks for a class named `handler`.

    The database is checked on the first request, not when the file is
    loaded, so the build step can import this module without a connection.
    """

    def handle(self):
        global _ready
        if not _ready:
            init_db()
            _ready = True
        super().handle()
