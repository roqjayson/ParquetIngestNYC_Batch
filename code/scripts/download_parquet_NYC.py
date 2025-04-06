import os
import re
import argparse
import pandas as pd
import requests
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
from tqdm import tqdm


# === Constants ===
BASE_FOLDER = "TLC_Parquet_Links"
DOWNLOADS_FOLDER = "TLC_Parquet_Downloads"
DESKTOP_PATH = Path.home() / "Desktop"


def find_latest_csv(base_path: Path) -> Path:
    """Grab the newest CSV file from nested folders."""
    all_csv_files = list(base_path.rglob("*.csv"))
    if not all_csv_files:
        raise FileNotFoundError("No CSV files found in the given directory.")
    return max(all_csv_files, key=os.path.getmtime)


def is_parquet(url: str) -> bool:
    """Check if URL ends with .parquet (case-insensitive)."""
    return url.lower().endswith('.parquet')


def extract_year_month_from_filename(filename: str) -> str:
    """Pull YYYY-MM from filename. Returns 'unknown' if not found."""
    match = re.search(r'(\d{4})-(\d{2})', filename)
    return match.group(0) if match else "unknown"


def is_within_range(ym: str, start: str, end: str) -> bool:
    """Check if a given YYYY-MM string is within a range."""
    return (start <= ym <= end)


def get_filename_from_url(url: str) -> str:
    """Get filename from full URL path."""
    return os.path.basename(urlparse(url).path)


def download_file(url: str, base_download_path: Path):
    """Download a single file to ~/Desktop/TLC_Parquet_Downloads/<YYYY>/<MM>/."""
    try:
        filename = get_filename_from_url(url)
        year_month = extract_year_month_from_filename(filename)
        year, month = year_month.split("-") if "-" in year_month else ("unknown", "unknown")

        target_folder = base_download_path / year / month
        target_folder.mkdir(parents=True, exist_ok=True)

        file_path = target_folder / filename

        
        if file_path.exists():
            local_size = file_path.stat().st_size
            remote_head = requests.head(url)
            remote_size = int(remote_head.headers.get("Content-Length", -1))
    
            if remote_size == local_size:
                print(f"⏭️ Skipped (already exists and matches size): {filename}")
                return
            else:
                print(f"🔁 Re-downloading (size mismatch): {filename}")

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Downloaded: {filename} → {target_folder}")

    except Exception as e:
        print(f"❌ Failed to download {url} - {e}")


def main():
    """CLI entry point to download NYC parquet files by date range or file limit."""
    parser = argparse.ArgumentParser(description="Download parquet files by date range or limit.")
    parser.add_argument("--start", type=str, help="Start date (YYYY-MM)", default="0000-00")
    parser.add_argument("--end", type=str, help="End date (YYYY-MM)", default="9999-12")
    parser.add_argument("--limit", type=int, help="Max number of files to download", default=None)
    args = parser.parse_args()

    try:
        parquet_links_folder = DESKTOP_PATH / BASE_FOLDER
        latest_csv = find_latest_csv(parquet_links_folder)
        print(f"📄 Found latest CSV: {latest_csv}")

        df = pd.read_csv(latest_csv)
        if "URL" not in df.columns:
            raise ValueError("CSV must contain a 'URL' column.")

        parquet_urls = df["URL"].dropna()
        filtered_urls = []

        for url in parquet_urls:
            if not is_parquet(url):
                continue
            filename = get_filename_from_url(url)
            year_month = extract_year_month_from_filename(filename)
            if is_within_range(year_month, args.start, args.end):
                filtered_urls.append(url)

        if not filtered_urls:
            print("⚠️ No matching .parquet files found in the given range.")
            return

        if args.limit:
            filtered_urls = filtered_urls[:args.limit]

        print(f"⬇️ Preparing to download {len(filtered_urls)} files...")
        base_download_dir = DESKTOP_PATH / DOWNLOADS_FOLDER

        for url in tqdm(filtered_urls):
            download_file(url, base_download_dir)

        print("🎉 Downloads complete.")

    except Exception as e:
        print(f"🚨 Error: {e}")


if __name__ == "__main__":
    main()