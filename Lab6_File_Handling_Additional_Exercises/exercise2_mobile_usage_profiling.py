
from pathlib import Path
import csv
import urllib.request
from collections import Counter
from statistics import mean

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

# 3. DOWNLOAD DATASET IF MISSING

INPUT_FILE = DATA_DIR / "user_behavior_dataset.csv"

DATASET_URL = (
    "https://raw.githubusercontent.com/"
    "GayatriSubramanium/"
    "Mobile-Device-Usage-and-User-Behavior-Dataset/"
    "main/user_behavior_dataset.csv"
)

if not INPUT_FILE.exists():
    print("\nDownloading mobile usage dataset...")

    try:
        urllib.request.urlretrieve(DATASET_URL, INPUT_FILE)
        print("Dataset downloaded successfully!")
    except Exception as error:
        raise RuntimeError(
            "Dataset download failed. Download "
            "user_behavior_dataset.csv manually from Kaggle "
            "and place it inside the data folder."
        ) from error

# 4. READ DATASET

with open(INPUT_FILE, "r", encoding="utf-8-sig",
          newline="") as file:

    reader = csv.DictReader(file)
    records = list(reader)

if not records:
    raise ValueError("The mobile usage CSV is empty.")

print("\nDataset successfully loaded!")
print("Total records:", len(records))
print("Columns:", list(records[0].keys()))


# 5. CLEAN AND CONVERT NUMERIC DATA

numeric_columns = [
    "App Usage Time (min/day)",
    "Screen On Time (hours/day)",
    "Battery Drain (mAh/day)",
    "Number of Apps Installed",
    "Data Usage (MB/day)",
    "Age",
    "User Behavior Class"
]

clean_records = []

for row in records:
    try:
        cleaned = dict(row)

        for column in numeric_columns:
            cleaned[column] = float(row[column])

        clean_records.append(cleaned)

    except (ValueError, TypeError, KeyError):
        continue

print("Valid records:", len(clean_records))
print("Incomplete records:", len(records) - len(clean_records))

if not clean_records:
    raise ValueError("No valid mobile usage records found.")

# 6. CALCULATE USAGE AVERAGES

app_usage = [
    row["App Usage Time (min/day)"]
    for row in clean_records
]

screen_time = [
    row["Screen On Time (hours/day)"]
    for row in clean_records
]

battery_drain = [
    row["Battery Drain (mAh/day)"]
    for row in clean_records
]

data_usage = [
    row["Data Usage (MB/day)"]
    for row in clean_records
]

average_app_usage = mean(app_usage)
average_screen_time = mean(screen_time)
average_battery_drain = mean(battery_drain)
average_data_usage = mean(data_usage)

# 7. ANALYZE DEVICE MODELS

device_counts = Counter(
    row["Device Model"] for row in clean_records
)

print("\nTOP DEVICE MODELS:")

for device, count in device_counts.most_common(5):
    print(device, "=", count, "users")

# 8. ANALYZE OPERATING SYSTEMS

os_counts = Counter(
    row["Operating System"] for row in clean_records
)

print("\nOPERATING SYSTEM SUMMARY:")

for operating_system, count in os_counts.items():
    print(operating_system, "=", count, "users")

# 9. ANALYZE USER BEHAVIOR CLASSES

behavior_counts = Counter(
    int(row["User Behavior Class"])
    for row in clean_records
)

print("\nUSER BEHAVIOR CLASSES:")

for behavior, count in sorted(behavior_counts.items()):
    print("Class", behavior, "=", count, "users")

# 10. DISPLAY AVERAGE USAGE

print("\nAVERAGE MOBILE USAGE:")
print("App Usage:", round(average_app_usage, 2), "minutes/day")
print("Screen Time:", round(average_screen_time, 2), "hours/day")
print("Battery Drain:", round(average_battery_drain, 2), "mAh/day")
print("Data Usage:", round(average_data_usage, 2), "MB/day")

# 11. SAVE CLEANED DATASET

CLEANED_FILE = OUTPUT_DIR / "cleaned_mobile_usage.csv"

with open(CLEANED_FILE, "w", encoding="utf-8",
          newline="") as file:

    fieldnames = list(clean_records[0].keys())
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(clean_records)

print("\nCleaned dataset saved:", CLEANED_FILE)

# 12. GENERATE ANALYSIS REPORT

REPORT_FILE = OUTPUT_DIR / (
    f"{LAST_NAME}_{STUDENT_ID}_mobile_report.txt"
)

with open(REPORT_FILE, "w", encoding="utf-8") as file:

    file.write("MOBILE USAGE PROFILING REPORT\n")
    file.write("=============================\n\n")

    file.write(f"Student: {LAST_NAME}\n")
    file.write(f"Student ID: {STUDENT_ID}\n")
    file.write(f"Seed Digit: {SEED_DIGIT}\n")
    file.write(f"ID Sum: {ID_SUM}\n\n")

    file.write("DATASET SUMMARY\n")
    file.write(f"Total records: {len(records)}\n")
    file.write(f"Valid records: {len(clean_records)}\n\n")

    file.write("AVERAGE MOBILE USAGE\n")
    file.write(f"App Usage: {average_app_usage:.2f} minutes/day\n")
    file.write(f"Screen Time: {average_screen_time:.2f} hours/day\n")
    file.write(f"Battery Drain: {average_battery_drain:.2f} mAh/day\n")
    file.write(f"Data Usage: {average_data_usage:.2f} MB/day\n\n")

    file.write("DEVICE MODEL SUMMARY\n")
    for device, count in device_counts.most_common():
        file.write(f"{device}: {count}\n")

    file.write("\nOPERATING SYSTEM SUMMARY\n")
    for operating_system, count in os_counts.items():
        file.write(f"{operating_system}: {count}\n")

    file.write("\nUSER BEHAVIOR CLASSES\n")
    for behavior, count in sorted(behavior_counts.items()):
        file.write(f"Class {behavior}: {count}\n")

print("Analysis report saved:", REPORT_FILE)

# 13. FINAL OUTPUT

print("\n================================")
print("MOBILE USAGE PROFILING COMPLETED!")
print("================================")
print("Total records:", len(records))
print("Valid records:", len(clean_records))
print("Cleaned CSV:", CLEANED_FILE)
print("Analysis report:", REPORT_FILE)