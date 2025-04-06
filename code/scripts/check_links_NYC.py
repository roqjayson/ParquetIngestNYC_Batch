import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List


# Constants
BASE_URL = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
DOWNLOAD_FOLDER_NAME = "TLC_Parquet_Links"


def fetch_html(url: str) -> str:
    """Fetch the HTML from a URL. Nothing fancy. Just GET it."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def extract_links(html: str, extensions: List[str]) -> List[str]:
    """
    Scrape all links from the HTML that match a list of extensions.
    You give me ['.parquet', '.pdf'] and I give you links with those.
    """
    soup = BeautifulSoup(html, 'html.parser')
    links = [
        a['href']
        for a in soup.find_all('a', href=True)
        if any(ext in a['href'] for ext in extensions)
    ]
    return links


def get_file_extension(url: str) -> str:
    """
    Pull the file extension from a URL and make it all caps.
    If there's no extension, we just call it 'OTHER'.
    """
    ext = os.path.splitext(url)[-1].lower()
    return ext[1:].upper() if ext.startswith('.') else 'OTHER'


def create_output_path(base_folder: str, timestamp: datetime) -> str:
    """
    Builds a folder path like ~/Desktop/base_folder/Y/M/D/H/M and makes sure it exists.
    Returns the full path. That’s it.
    """
    time_parts = [timestamp.strftime(part) for part in ['%Y', '%m', '%d', '%H', '%M']]
    full_path = os.path.join(os.path.expanduser("~"), "Desktop", base_folder, *time_parts)
    os.makedirs(full_path, exist_ok=True)
    return full_path


def save_links_to_csv(links: List[str], folder_path: str, timestamp: datetime):
    """
    Dumps the links to a CSV. Includes file extension and timestamp.
    CSV lands in the folder_path you gave me.
    """
    filename = f"parquet_links_{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    filepath = os.path.join(folder_path, filename)

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Extension", "Time Scanned"])
        scan_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        for link in links:
            extension = get_file_extension(link)
            writer.writerow([link, extension, scan_time])
    
    print(f"CSV file saved at: {filepath}")


def main():
    """
    Main script runner.
    Grabs the HTML, pulls out parquet/pdf links, saves them to a timestamped CSV.
    Folders are organized by datetime. Neat and tidy.
    """
    html = fetch_html(BASE_URL)
    links = extract_links(html, extensions=['.parquet', '.pdf'])
    timestamp = datetime.now()
    output_folder = create_output_path(DOWNLOAD_FOLDER_NAME, timestamp)
    save_links_to_csv(links, output_folder, timestamp)


if __name__ == "__main__":
    main()