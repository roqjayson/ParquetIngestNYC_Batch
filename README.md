# ParquetIngestNYC_Batch
This project automates the process of downloading Parquet files from the NYC Taxi Trip Record Data. It is structured in multiple phases to separate concerns and improve maintainability.

## 🧩 Project Phases
### ✅ Phase 1: Link Extraction

- Scrapes all downloadable Parquet file URLs from the NYC Taxi Records webpage.
- Saves the list of URLs into a CSV file.
- The CSV is stored in a subfolder based on the timestamp it was created (e.g., data/2024/04/05/sample.csv).

### ⏳ Phase 2: File Download (Coming Soon)
- Reads the CSV from Phase 1.
- Downloads each Parquet file and saves it to organized folders based on their time period.
- Allows parameterized execution by either limiting the number of files to be downloaded or limiting the date range of download.

## 🛠️ Tech Stack
- **Language**: Python
- **Libraries**: See requirements/requirements.txt

## 📁 Project Structure

ParquetIngestNYC_Batch/
```
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
  
### Execution
- Fork repo and then run the script `chck_and_download.py`
- Logs are found in /logs folder (no datetime attached to the log file yet)


### 📌 Notes
- Make sure you have enough local storage for the downloaded CSV/Parquet files.
- Large datasets can take time and bandwidth to download.
