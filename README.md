# ParquetIngestNYC_Batch
This project automates the process of downloading Parquet files from the NYC Taxi Trip Record Data. It is structured in multiple phases to separate concerns and improve maintainability.

## 🧩 Project Phases
### ✅ Phase 1: Link Extraction

- Scrapes all downloadable Parquet file URLs from the NYC Taxi Records webpage.
- Saves the list of URLs into a CSV file.
- The CSV is stored in a subfolder based on the timestamp it was created (e.g., data/2024/04/05/sample.csv).

### ⏳ Phase 2: File Download (Coming Soon)
- Will read the CSV file from Phase 1.
- Downloads each Parquet file and saves it to organized folders based on their category or time period.

## 🛠️ Tech Stack
- **Language**: Python
- **Libraries**: requests, BeautifulSoup, os, csv. (Might be updated in the future)

## 📁 Project Structure

ParquetIngestNYC_Batch/
```
├── data
│   └── YYYY
|       └── MM
|           └── DD
|               └── HH
|                    └── MM
│                       └── available_links.csv
├── code
|    └── script
|        └── check_links_NYC.py
|    └── requirements
|        └── requirements.txt
├── README.md

```
## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Install dependencies:

  ```bash
  pip install -r requirements/requirements.txt
  ```
  
### Run Phase 1

 ```python
 python check_links_NYC.py 
 ```
 - This will generate a CSV file containing all download links found on the NYC Taxi Data website.
 - The CSV is automatically saved in a timestamped folder under your local desktop. (It will be improved with having the file stored in the repo folder.


### 📌 Notes
- Make sure you have enough local storage for the downloaded CSV/Parquet files.
- Large datasets can take time and bandwidth to download.
