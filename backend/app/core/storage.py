from pathlib import Path

UPLOAD_DIR = Path("app/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)