
from pathlib import Path
import csv
import urllib.request
from collections import Counter
from datetime import datetime

# 1. STUDENT CONFIGURATION

LAST_NAME = "MARJES"
STUDENT_ID = "TUPM-26-1948"

digits = [int(d) for d in STUDENT_ID if d.isdigit()]

if not digits:
    raise ValueError("Enter your actual Student ID containing numbers.")

SEED_DIGIT = digits[-1]
ID_SUM = sum(digits)
NAME_LENGTH = len(LAST_NAME)

print("Student:", LAST_NAME)
print("Student ID:", STUDENT_ID)
print("Seed Digit:", SEED_DIGIT)
print("ID Sum:", ID_SUM)

# 2. CREATE PROJECT FOLDERS

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
BACKUP_DIR = BASE_DIR / "backup"

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

# 3. DOWNLOAD WEB LOG DATASET IF MISSING

INPUT_FILE = DATA_DIR / "weblog.csv"

DATASET_URL = (
    "https://raw.githubusercontent.com/"
    "shawon100/Web-Log-Dataset/master/weblog.csv"
)

if not INPUT_FILE.exists():
    print("\nDataset not found. Downloading...")

    try:
        urllib.request.urlretrieve(DATASET_URL, INPUT_FILE)
        print("Dataset downloaded successfully!")
    except Exception as error:
        raise RuntimeError(
            "Could not download the dataset. "
            "Check your internet connection or download "
            "weblog.csv manually from Kaggle."
        ) from error

print("Dataset location:", INPUT_FILE)

# 4. READ WEB LOG DATASET

with open(INPUT_FILE, "r", encoding="utf-8-sig",
          newline="") as file:

    reader = csv.DictReader(file)
    records = list(reader)

if not records:
    raise ValueError("The CSV file is empty.")

print("\nDataset successfully loaded!")
print("Total records:", len(records))
print("Columns:", list(records[0].keys()))

# 5. CLEAN AND ORGANIZE DATA

clean_records = []

for row in records:

    ip = row.get("IP", "").strip()
    time = row.get("Time", "").strip()
    url = row.get("URL", "").strip()

    # Dataset uses the original column name "Staus"
    status = row.get("Staus", "").strip()

    if not status:
        status = row.get("Status", "").strip()

    if ip and time and url and status:
        clean_records.append({
            "IP": ip,
            "Time": time,
            "URL": url,
            "Status": status
        })

print("Valid records:", len(clean_records))
print("Removed incomplete records:",
      len(records) - len(clean_records))

# 6. ANALYZE IP ADDRESSES

ip_counts = Counter(
    row["IP"] for row in clean_records
)

print("\nTOP 5 IP ADDRESSES:")

for ip, count in ip_counts.most_common(5):
    print(ip, "=", count, "requests")

# 7. ANALYZE REQUESTED URLS

url_counts = Counter(
    row["URL"] for row in clean_records
)

print("\nTOP 5 REQUESTED URLS:")

for url, count in url_counts.most_common(5):
    print(url, "=", count, "requests")

# 8. ANALYZE HTTP STATUS CODES

status_counts = Counter(
    row["Status"] for row in clean_records
)

print("\nHTTP STATUS CODE SUMMARY:")

for status, count in sorted(status_counts.items()):
    print(status, "=", count, "requests")

error_count = sum(
    count for status, count in status_counts.items()
    if status.isdigit() and int(status) >= 400
)

success_count = sum(
    count for status, count in status_counts.items()
    if status.isdigit() and 200 <= int(status) < 300
)

print("\nSuccessful requests:", success_count)
print("Error requests:", error_count)

# 9. ANALYZE REQUEST TIMES

hours = []

for row in clean_records:
    try:
        time_value = row["Time"].lstrip("[")

        request_time = datetime.strptime(
            time_value,
            "%d/%b/%Y:%H:%M:%S"
        )

        hours.append(request_time.hour)

    except ValueError:
        continue

hour_counts = Counter(hours)

print("\nREQUESTS PER HOUR:")

for hour, count in sorted(hour_counts.items()):
    print(f"{hour:02d}:00 - {count} requests")

if hour_counts:
    busiest_hour, busiest_count = hour_counts.most_common(1)[0]
else:
    busiest_hour = None
    busiest_count = 0

# 10. SAVE CLEANED DATASET

CLEANED_FILE = OUTPUT_DIR / "cleaned_weblog.csv"

with open(CLEANED_FILE, "w", encoding="utf-8",
          newline="") as file:

    fieldnames = ["IP", "Time", "URL", "Status"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(clean_records)

print("\nCleaned dataset saved:", CLEANED_FILE)

# 11. CREATE ANALYSIS REPORT

REPORT_FILE = OUTPUT_DIR / (
    f"{LAST_NAME}_{STUDENT_ID}_web_log_report.txt"
)

with open(REPORT_FILE, "w", encoding="utf-8") as file:

    file.write("WEB LOG ANALYSIS REPORT\n")
    file.write("=======================\n\n")

    file.write(f"Student: {LAST_NAME}\n")
    file.write(f"Student ID: {STUDENT_ID}\n")
    file.write(f"Seed Digit: {SEED_DIGIT}\n")
    file.write(f"ID Sum: {ID_SUM}\n\n")

    file.write("DATASET SUMMARY\n")
    file.write(f"Total records: {len(records)}\n")
    file.write(f"Valid records: {len(clean_records)}\n")
    file.write(
        f"Incomplete records: "
        f"{len(records) - len(clean_records)}\n\n"
    )

    file.write("TOP 5 IP ADDRESSES\n")

    for ip, count in ip_counts.most_common(5):
        file.write(f"{ip}: {count}\n")

    file.write("\nTOP 5 REQUESTED URLS\n")

    for url, count in url_counts.most_common(5):
        file.write(f"{url}: {count}\n")

    file.write("\nHTTP STATUS CODES\n")

    for status, count in sorted(status_counts.items()):
        file.write(f"{status}: {count}\n")

    file.write(f"\nSuccessful requests: {success_count}\n")
    file.write(f"Error requests: {error_count}\n")

    file.write("\nREQUESTS PER HOUR\n")

    for hour, count in sorted(hour_counts.items()):
        file.write(f"{hour:02d}:00 - {count}\n")

    if busiest_hour is not None:
        file.write(
            f"\nBusiest hour: {busiest_hour:02d}:00 "
            f"({busiest_count} requests)\n"
        )

print("\nAnalysis report saved:", REPORT_FILE)

# 12. FINAL OUTPUT

print("\n================================")
print("WEB LOG ANALYSIS COMPLETED!")
print("================================")
print("Total records:", len(records))
print("Valid records:", len(clean_records))
print("Successful requests:", success_count)
print("Error requests:", error_count)
print("Cleaned CSV:", CLEANED_FILE)
print("Analysis report:", REPORT_FILE)