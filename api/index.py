"""Vercel serverless entrypoint for the Flask application."""

import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Vercel imports this module and looks for a top-level WSGI app named `app`.
os.environ.setdefault("VERCEL", "1")

from app import app  # noqa: E402
