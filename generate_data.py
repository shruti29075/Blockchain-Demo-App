#-------------------- FOR BLOCKCHAIN LEDGER

import pandas as pd
import hashlib
import random
import datetime

# File name for CSV storage
CSV_FILE = "hospital_ledger.csv"

# Predefined scan types & body parts
SCAN_TYPES = ["CT Scan", "X-Ray", "MRI", "Ultrasound"]
BODY_PARTS = ["Head", "Chest", "Abdomen", "Spine", "Leg", "Arm", "Pelvis"]

# Sample names to generate records
PATIENT_NAMES = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Hannah", "Ian", "Jack", 
                 "Kylie", "Liam", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Ryan", "Sophia", "Tom", 
                 "Uma", "Victor", "Will", "Xander", "Yasmine", "Zack"]

# Function to generate a hash for patient names
def generate_hash(patient_name):
    return hashlib.sha256(patient_name.lower().encode()).hexdigest()

# Function to create a unique transaction hash
def generate_transaction_hash(patient_name, scan_type, body_part, cost, date_of_visit):
    data_string = f"{patient_name.lower()}-{scan_type}-{body_part}-{cost}-{date_of_visit}"
    return hashlib.sha256(data_string.encode()).hexdigest()

# Generate 100 random patient records
records = []
for _ in range(100):
    patient_name = random.choice(PATIENT_NAMES)
    scan_type = random.choice(SCAN_TYPES)
    body_part = random.choice(BODY_PARTS)
    cost = round(random.uniform(50, 500), 2)  # Random cost between $50 and $500
    date_of_visit = datetime.date.today() - datetime.timedelta(days=random.randint(1, 365))  # Random date in the past year

    patient_hash = generate_hash(patient_name)
    transaction_hash = generate_transaction_hash(patient_name, scan_type, body_part, cost, date_of_visit)

    records.append([patient_hash, scan_type, body_part, cost, date_of_visit, transaction_hash])

# Save to CSV
df = pd.DataFrame(records, columns=["Patient_Hash", "Scan_Type", "Body_Part", "Cost", "Date_of_Visit", "Transaction_Hash"])
df.to_csv(CSV_FILE, index=False)

print(f"✅ Successfully generated {len(df)} patient records and saved to {CSV_FILE}")

