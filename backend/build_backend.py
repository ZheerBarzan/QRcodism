import os
import subprocess
import sys
from pathlib import Path


def _platform_folder() -> str:
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "mac"
    return "linux"


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    backend_dir = Path(__file__).resolve().parent
    output_dir = repo_root / "desktop" / "resources" / "backend" / _platform_folder()
    work_dir = backend_dir / "build" / "pyinstaller"
    spec_dir = backend_dir / "build"

    output_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)
    spec_dir.mkdir(parents=True, exist_ok=True)

    desktop_server = backend_dir / "desktop_server.py"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",
        "--name",
        "qrcodism-backend",
        "--distpath",
        str(output_dir),
        "--workpath",
        str(work_dir),
        "--specpath",
        str(spec_dir),
        "--collect-submodules",
        "backend",
        "--collect-submodules",
        "core",
        str(desktop_server),
    ]

    print("Building backend with PyInstaller...")
    print(" ".join(cmd))
    return subprocess.call(cmd, cwd=str(backend_dir))


if __name__ == "__main__":
    raise SystemExit(main())
