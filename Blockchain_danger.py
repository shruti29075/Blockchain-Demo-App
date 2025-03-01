import streamlit as st
import pandas as pd
import hashlib
import time
import os
import json

# File to store blockchain data
BLOCKCHAIN_FILE = "blockchain.json"
CSV_FILE = "hospital_ledger.csv"

# Predefined scan types & body parts
SCAN_TYPES = ["CT Scan", "X-Ray", "MRI", "Ultrasound"]
BODY_PARTS = ["Head", "Chest", "Abdomen", "Spine", "Leg", "Arm", "Pelvis"]

def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def load_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as file:
            return json.load(file)
    return []

def save_blockchain(blockchain):
    with open(BLOCKCHAIN_FILE, "w") as file:
        json.dump(blockchain, file, indent=4)

def create_block(transaction_data):
    blockchain = load_blockchain()
    previous_hash = blockchain[-1]['hash'] if blockchain else "0"
    block = {
        "index": len(blockchain) + 1,
        "timestamp": time.ctime(),
        "transaction": transaction_data,
        "previous_hash": previous_hash,
    }
    block["hash"] = generate_hash(json.dumps(block, sort_keys=True))
    blockchain.append(block)
    save_blockchain(blockchain)

def add_patient():
    st.subheader("Add Patient Record")
    name = st.text_input("Patient Name").strip().lower()
    scan_type = st.selectbox("Scan Type", SCAN_TYPES)
    body_part = st.selectbox("Body Part", BODY_PARTS)
    cost = st.number_input("Cost of Scan ($)", min_value=0.0, format="%.2f")
    date_of_visit = st.date_input("Date of Visit")

    if st.button("Add Record"):
        patient_hash = generate_hash(name)
        transaction = {
            "patient_name": name,  # Storing actual patient name for retrieval
            "patient_hash": patient_hash,
            "scan_type": scan_type,
            "body_part": body_part,
            "cost": cost,
            "date_of_visit": str(date_of_visit)
        }
        create_block(transaction)
        st.success("Record added to the blockchain!")

def view_blockchain():
    st.subheader("Blockchain Ledger")
    blockchain = load_blockchain()
    if blockchain:
        for block in blockchain:
            st.json(block, expanded=False)
    else:
        st.warning("Blockchain is empty!")

def search_records():
    st.subheader("Search Patient Records")
    search_query = st.text_input("Enter Patient Name to Search:").strip().lower()

    if search_query:
        blockchain = load_blockchain()  # Load blockchain here
        found_records = []

        for block in blockchain:
            transaction = block.get("transaction", {})  # Safely get transaction dict
            patient_name = transaction.get("patient_name", "").lower()  # Get name safely

            if search_query == patient_name:
                found_records.append(block)

        if found_records:
            st.write("### Search Results:")
            for record in found_records:
                st.json(record)
        else:
            st.warning("No records found for this patient.")



def delete_record():
    st.subheader("Delete a Record (Demo Purpose)")
    delete_index = st.number_input("Enter Block Index to Delete", min_value=1, step=1)
    if st.button("Delete Block"):
        blockchain = load_blockchain()
        blockchain = [block for block in blockchain if block['index'] != delete_index]
        for i, block in enumerate(blockchain):
            block['index'] = i + 1
        save_blockchain(blockchain)
        st.warning(f"Block {delete_index} deleted! (In real blockchain, this would cause a fork)")

def main():
    st.title("Hospital Ledger - Blockchain Implementation")
    menu = ["Add Patient", "View Blockchain", "Search Records", "Delete Record"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add Patient":
        add_patient()
    elif choice == "View Blockchain":
        view_blockchain()
    elif choice == "Search Records":
        search_records()
    elif choice == "Delete Record":
        delete_record()

if __name__ == "__main__":
    main()
