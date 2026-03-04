import os

from .settings import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CORS_ALLOW_ALL_ORIGINS = True

qr_data_dir = os.getenv("QR_DATA_DIR")
qr_db_path = os.getenv("QR_DB_PATH")

if qr_db_path:
    DATABASES["default"]["NAME"] = qr_db_path
elif qr_data_dir:
    DATABASES["default"]["NAME"] = os.path.join(qr_data_dir, "db.sqlite3")
else:
    DATABASES["default"]["NAME"] = ":memory:"
