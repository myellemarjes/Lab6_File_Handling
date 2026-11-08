
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

INPUT_FILE = DATA_DIR / "Global_Cybersecurity_Threats_2015-2024.csv"

DATASET_URL = (
    "https://raw.githubusercontent.com/"
    "FlazeFy2/DS-Global_Cybersecurity_Threats/"
    "main/Global_Cybersecurity_Threats_2015-2024.csv"
)

if not INPUT_FILE.exists():
    print("\nDownloading cybersecurity dataset...")

    try:
        urllib.request.urlretrieve(DATASET_URL, INPUT_FILE)
        print("Dataset downloaded successfully!")

    except Exception as error:
        raise RuntimeError(
            "Dataset download failed. Download the CSV "
            "manually from Kaggle and place it inside "
            "the data folder."
        ) from error

# 4. READ DATASET

with open(INPUT_FILE, "r", encoding="utf-8-sig",
          newline="") as file:

    reader = csv.DictReader(file)
    records = list(reader)

if not records:
    raise ValueError("The cybersecurity CSV is empty.")

print("\nDataset successfully loaded!")
print("Total records:", len(records))
print("Columns:", list(records[0].keys()))

# 5. CLEAN AND CONVERT DATA

numeric_columns = [
    "Year",
    "Financial Loss (in Million $)",
    "Number of Affected Users",
    "Incident Resolution Time (in Hours)"
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
    raise ValueError("No valid cybersecurity records found.")

# 6. ANALYZE ATTACK TYPES

attack_counts = Counter(
    row["Attack Type"] for row in clean_records
)

print("\nATTACK TYPE SUMMARY:")

for attack, count in attack_counts.most_common():
    print(attack, "=", count, "incidents")

# 7. ANALYZE TARGET INDUSTRIES

industry_counts = Counter(
    row["Target Industry"] for row in clean_records
)

print("\nTARGET INDUSTRY SUMMARY:")

for industry, count in industry_counts.most_common():
    print(industry, "=", count, "incidents")

# 8. ANALYZE ATTACK SOURCES

source_counts = Counter(
    row["Attack Source"] for row in clean_records
)

print("\nATTACK SOURCE SUMMARY:")

for source, count in source_counts.most_common():
    print(source, "=", count, "incidents")

# 9. ANALYZE SECURITY VULNERABILITIES

vulnerability_counts = Counter(
    row["Security Vulnerability Type"]
    for row in clean_records
)

print("\nSECURITY VULNERABILITY SUMMARY:")

for vulnerability, count in vulnerability_counts.most_common():
    print(vulnerability, "=", count, "incidents")

# 10. CALCULATE FINANCIAL AND USER IMPACT

financial_losses = [
    row["Financial Loss (in Million $)"]
    for row in clean_records
]

affected_users = [
    row["Number of Affected Users"]
    for row in clean_records
]

resolution_times = [
    row["Incident Resolution Time (in Hours)"]
    for row in clean_records
]

average_loss = mean(financial_losses)
total_loss = sum(financial_losses)

average_affected_users = mean(affected_users)
total_affected_users = sum(affected_users)

average_resolution_time = mean(resolution_times)

print("\nINCIDENT IMPACT SUMMARY:")
print("Total financial loss: $", round(total_loss, 2), "million")
print("Average financial loss: $", round(average_loss, 2), "million")
print("Total affected users:", int(total_affected_users))
print("Average affected users:", round(average_affected_users, 2))
print("Average resolution time:", round(average_resolution_time, 2), "hours")

# 11. ANALYZE INCIDENTS BY YEAR

year_counts = Counter(
    int(row["Year"]) for row in clean_records
)

print("\nINCIDENTS PER YEAR:")

for year, count in sorted(year_counts.items()):
    print(year, "=", count, "incidents")

# 12. ANALYZE DEFENSE MECHANISMS

defense_counts = Counter(
    row["Defense Mechanism Used"]
    for row in clean_records
)

print("\nDEFENSE MECHANISM SUMMARY:")

for defense, count in defense_counts.most_common():
    print(defense, "=", count, "incidents")

# 13. SAVE CLEANED DATASET

CLEANED_FILE = OUTPUT_DIR / "cleaned_cybersecurity_data.csv"

with open(CLEANED_FILE, "w", encoding="utf-8",
          newline="") as file:

    fieldnames = list(clean_records[0].keys())
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(clean_records)

print("\nCleaned dataset saved:", CLEANED_FILE)

# 14. GENERATE CYBERSECURITY REPORT

REPORT_FILE = OUTPUT_DIR / (
    f"{LAST_NAME}_{STUDENT_ID}_cybersecurity_report.txt"
)

with open(REPORT_FILE, "w", encoding="utf-8") as file:

    file.write("CYBERSECURITY INCIDENT REPORT\n")
    file.write("=============================\n\n")

    file.write(f"Student: {LAST_NAME}\n")
    file.write(f"Student ID: {STUDENT_ID}\n")
    file.write(f"Seed Digit: {SEED_DIGIT}\n")
    file.write(f"ID Sum: {ID_SUM}\n\n")

    file.write("DATASET SUMMARY\n")
    file.write(f"Total records: {len(records)}\n")
    file.write(f"Valid records: {len(clean_records)}\n\n")

    file.write("ATTACK TYPES\n")
    for attack, count in attack_counts.most_common():
        file.write(f"{attack}: {count}\n")

    file.write("\nTARGET INDUSTRIES\n")
    for industry, count in industry_counts.most_common():
        file.write(f"{industry}: {count}\n")

    file.write("\nATTACK SOURCES\n")
    for source, count in source_counts.most_common():
        file.write(f"{source}: {count}\n")

    file.write("\nSECURITY VULNERABILITIES\n")
    for vulnerability, count in vulnerability_counts.most_common():
        file.write(f"{vulnerability}: {count}\n")

    file.write("\nFINANCIAL AND USER IMPACT\n")
    file.write(f"Total financial loss: ${total_loss:.2f} million\n")
    file.write(f"Average financial loss: ${average_loss:.2f} million\n")
    file.write(f"Total affected users: {int(total_affected_users)}\n")
    file.write(f"Average affected users: {average_affected_users:.2f}\n")
    file.write(f"Average resolution time: {average_resolution_time:.2f} hours\n")

    file.write("\nINCIDENTS PER YEAR\n")
    for year, count in sorted(year_counts.items()):
        file.write(f"{year}: {count}\n")

    file.write("\nDEFENSE MECHANISMS\n")
    for defense, count in defense_counts.most_common():
        file.write(f"{defense}: {count}\n")

print("Cybersecurity report saved:", REPORT_FILE)

# 15. FINAL OUTPUT

print("\n================================")
print("CYBERSECURITY INCIDENT ANALYSIS COMPLETED!")
print("================================")
print("Total records:", len(records))
print("Valid records:", len(clean_records))
print("Total financial loss: $", round(total_loss, 2), "million")
print("Average resolution time:", round(average_resolution_time, 2), "hours")
print("Cleaned CSV:", CLEANED_FILE)
print("Analysis report:", REPORT_FILE)