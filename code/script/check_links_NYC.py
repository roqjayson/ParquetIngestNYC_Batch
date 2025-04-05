import os
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# URL of the TLC Trip Record Data page
url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Finds all links to parquet files and place them in a list
parquet_links = []

for a_tag in soup.find_all('a', href=True):
    if 'parquet' in a_tag['href'] or 'pdf' in a_tag['href']:  # Include .parquet and .pdf links
        parquet_links.append(a_tag['href'])

# Gets file extension type dynamically
def get_file_extension(url):
    # Extract file extension from the URL
    ext = os.path.splitext(url)[-1].lower()
    
    # Return extension after the dot (excluding the dot itself)
    if ext and ext.startswith('.'):
        return ext[1:].upper()  # Remove the dot and return the extension in uppercase
    else:
        return 'OTHER'  # Default case for links without an extension

# Gets the current time for folder structure and timestamped filename
current_time = datetime.now()
year = current_time.strftime('%Y')
month = current_time.strftime('%m')
day = current_time.strftime('%d')
hour = current_time.strftime('%H')
minute = current_time.strftime('%M')
scan_time = current_time.strftime('%Y-%m-%d %H:%M:%S')  # For timestamp in CSV

# Defines the folder structure based on Year/Month/Day/Hour/Minute
base_folder = os.path.join(os.path.expanduser("~"), "Desktop", "TLC_Parquet_Links", year, month, day, hour, minute)

# Creates the nested folders if they don't exist, but will not overwrite any existing ones
os.makedirs(base_folder, exist_ok=True)

# Generates the filename with timestamp
csv_file_name = f"parquet_links_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
csv_file_path = os.path.join(base_folder, csv_file_name)

# Writes the links, extension type, and timestamp to the CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Writes the header
    writer.writerow(["URL", "Extension", "Time Scanned"])
    
    # Writes the URLs, extension type, and the timestamp
    for link in parquet_links:
        extension = get_file_extension(link)
        writer.writerow([link, extension, scan_time])

print(f"CSV file saved at: {csv_file_path}")
