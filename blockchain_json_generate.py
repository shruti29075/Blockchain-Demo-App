import json
import hashlib
import random
import time
from datetime import datetime, timedelta

# Constants
SCAN_TYPES = ["CT Scan", "X-Ray", "MRI", "Ultrasound"]
BODY_PARTS = ["Head", "Chest", "Abdomen", "Spine", "Leg", "Arm", "Pelvis"]

# Function to generate a SHA-256 hash
def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Function to generate random patient data
def generate_random_transaction():
    patient_name = f"Patient_{random.randint(1, 1000)}" if random.random() > 0.1 else ""  # 10% chance of empty name
    patient_hash = generate_hash(patient_name) if patient_name else generate_hash("")  # Handle empty name case
    scan_type = random.choice(SCAN_TYPES)
    body_part = random.choice(BODY_PARTS)
    cost = round(random.uniform(100, 2000), 2)  # Random cost between $100 - $2000
    date_of_visit = (datetime.today() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")  # Random past date
    return {
        "patient_name": patient_name,
        "patient_hash": patient_hash,
        "scan_type": scan_type,
        "body_part": body_part,
        "cost": cost,
        "date_of_visit": date_of_visit
    }

# Function to generate blockchain records
def generate_blockchain(num_records=10):
    blockchain = []
    previous_hash = "0"

    for i in range(1, num_records + 1):
        transaction = generate_random_transaction()
        timestamp = time.ctime()
        block = {
            "index": i,
            "timestamp": timestamp,
            "transaction": transaction,
            "previous_hash": previous_hash,
        }
        block["hash"] = generate_hash(json.dumps(block, sort_keys=True))
        blockchain.append(block)
        previous_hash = block["hash"]  # Update previous hash for next block

    return blockchain

# Generate and save blockchain data
num_records = int(input("Enter the number of records to generate: "))
blockchain_data = generate_blockchain(num_records)

with open("generated_blockchain.json", "w") as file:
    json.dump(blockchain_data, file, indent=4)

print(f"{num_records} blockchain records generated and saved to 'generated_blockchain.json'.")
