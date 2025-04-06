"""
This script executes the check_links_NYC.py and download_parquet_NYC.py

Author: Jayson Roque
"""

import subprocess
import shutil
import argparse
import logging
import sys
import os
from pathlib import Path

# === Paths ===
BASE_DIR = Path(__file__).parent
SCRIPTS_DIR = BASE_DIR / "scripts"
REQUIREMENTS_FILE = BASE_DIR / "requirements" / "requirements.txt"
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "run_all.log"

# === Python Executable from .venv ===
VENV_PYTHON = (BASE_DIR.parent / ".venv" / "Scripts" / "python.exe").resolve()
if not VENV_PYTHON.exists():
    logging.warning("⚠️ .venv not found, falling back to system Python")
    VENV_PYTHON = shutil.which("python")

# === Logging Setup ===
LOGS_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='[%(asctime)s] %(levelname)s - %(message)s',
    level=logging.INFO
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def install_requirements():
    """Ensure all required packages are installed from requirements.txt."""
    try:
        if REQUIREMENTS_FILE.exists():
            logging.info("Installing requirements...")
            subprocess.run(
                [str(VENV_PYTHON), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
                check=True
            )
            logging.info("✅ Requirements installed successfully.")
        else:
            logging.warning(f"⚠️ No requirements.txt found at {REQUIREMENTS_FILE}")
    except subprocess.CalledProcessError as e:
        logging.error(f"🚨 Failed to install requirements: {e}")
        sys.exit(1)


def run_check_links():
    """Run Phase 1: check_links_NYC.py"""
    try:
        logging.info("🚀 Running Phase 1: check_links_NYC.py")
        subprocess.run([str(VENV_PYTHON), str(SCRIPTS_DIR / "check_links_NYC.py")], check=True)
        logging.info("✅ Phase 1 complete.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error in Phase 1: {e}")
        sys.exit(1)


def run_download_parquet(start: str, end: str, limit: int):
    """Run Phase 2: download_parquet_NYC.py with parameters"""
    try:
        logging.info("📥 Running Phase 2: download_parquet_NYC.py")

        cmd = [str(VENV_PYTHON), str(SCRIPTS_DIR / "download_parquet_NYC.py")]
        if start:
            cmd.extend(["--start", start])
        if end:
            cmd.extend(["--end", end])
        if limit:
            cmd.extend(["--limit", str(limit)])

        logging.info(f"📤 Phase 2 command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        logging.info("✅ Phase 2 complete.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error in Phase 2: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Run full pipeline: Check links + Download parquet files")
    parser.add_argument("--start", type=str, help="Start date (YYYY-MM)", default=None)
    parser.add_argument("--end", type=str, help="End date (YYYY-MM)", default=None)
    parser.add_argument("--limit", type=int, help="Limit number of files downloaded", default=None)
    args = parser.parse_args()

    logging.info("🏁 Starting ParquetIngestNYC_Batch full pipeline execution...")

    install_requirements()
    run_check_links()
    run_download_parquet(args.start, args.end, args.limit)

    logging.info("🎉 All tasks completed successfully!")


if __name__ == "__main__":
    main()