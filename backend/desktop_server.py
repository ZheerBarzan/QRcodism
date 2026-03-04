import argparse
import os
from pathlib import Path

def _parse_args():
    parser = argparse.ArgumentParser(description="QRcodism desktop backend server")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind (default: 8000)")
    parser.add_argument(
        "--data-dir",
        type=str,
        default="",
        help="Writable data directory for DB and runtime files",
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    if args.data_dir:
        data_dir = Path(args.data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("QR_DATA_DIR", str(data_dir))
        os.environ.setdefault("QR_DB_PATH", str(data_dir / "db.sqlite3"))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings_desktop")

    from backend.wsgi import application
    from waitress import serve

    serve(application, host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
