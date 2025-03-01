import streamlit as st
import pandas as pd
import hashlib
import os
import datetime

# File name for CSV storage
CSV_FILE = "hosptital_ledger.csv"

# Predefined scan types & body parts
SCAN_TYPES = ["CT Scan", "X-Ray", "MRI", "Ultrasound"]
BODY_PARTS = ["Head", "Chest", "Abdomen", "Spine", "Leg", "Arm", "Pelvis"]

# Function to generate a hash (for patient names)
def generate_hash(patient_name):
    return hashlib.sha256(patient_name.lower().encode()).hexdigest()

# Function to create a unique transaction hash (demonstrating blockchain)
def generate_transaction_hash(patient_name, scan_type, body_part, cost, date_of_visit):
    data_string = f"{patient_name.lower()}-{scan_type}-{body_part}-{cost}-{date_of_visit}"
    return hashlib.sha256(data_string.encode()).hexdigest()

# Function to load the hospital ledger
def load_ledger():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Patient_Hash", "Scan_Type", "Body_Part", "Cost", "Date_of_Visit", "Transaction_Hash"])

# Function to save the hospital ledger
def save_ledger(df):
    df.to_csv(CSV_FILE, index=False)

# Function to add a new patient visit
def add_patient_visit():
    st.subheader("🆕 Add Patient Visit")
    patient_name = st.text_input("Enter Patient's Name:").strip()
    scan_type = st.selectbox("Select Scan Type:", SCAN_TYPES)
    body_part = st.selectbox("Select Body Part:", BODY_PARTS)
    cost = st.number_input("Enter Cost ($):", min_value=0.0, format="%.2f")
    date_of_visit = st.date_input("Select Date of Visit", datetime.date.today())

    if st.button("Add Visit"):
        if patient_name:
            df = load_ledger()
            patient_hash = generate_hash(patient_name)
            transaction_hash = generate_transaction_hash(patient_name, scan_type, body_part, cost, date_of_visit)

            new_entry = pd.DataFrame(
                [[patient_hash, scan_type, body_part, cost, date_of_visit, transaction_hash]],
                columns=["Patient_Hash", "Scan_Type", "Body_Part", "Cost", "Date_of_Visit", "Transaction_Hash"]
            )

            df = pd.concat([df, new_entry], ignore_index=True)
            save_ledger(df)

            st.success(f"Visit added for **{patient_name}** (Stored as Hash: `{patient_hash}`)")
            st.info(f"Blockchain Transaction Hash: `{transaction_hash}`")
        else:
            st.error("⚠️ Please enter a valid patient name.")

# Function to search for a patient's visits (case-insensitive)
def search_patient_visits():
    st.subheader("🔍 Search Patient Records")
    patient_name = st.text_input("Enter Patient's Name to Search:").strip()

    if st.button("Search"):
        df = load_ledger()
        if patient_name:
            patient_hash = generate_hash(patient_name)
            filtered_df = df[df["Patient_Hash"] == patient_hash]

            if not filtered_df.empty:
                st.write(f"📄 Records for **{patient_name}**:")
                st.dataframe(filtered_df)
            else:
                st.warning(f"No records found for **{patient_name}**.")
        else:
            st.error("⚠️ Please enter a patient name.")

# Function to display all records
def retrieve_all_records():
    st.subheader("📜 Retrieve Full Ledger")
    df = load_ledger()

    if df.empty:
        st.warning("⚠️ No records found in the ledger.")
    else:
        st.write("✅ **Complete Hospital Ledger:**")
        st.dataframe(df)

# Function to delete a patient's records (case-insensitive)
def delete_patient_record():
    st.subheader("🗑️ Delete Patient Records")
    patient_name = st.text_input("Enter Patient's Name to Delete:").strip()

    if st.button("Delete"):
        df = load_ledger()
        if patient_name:
            patient_hash = generate_hash(patient_name)
            filtered_df = df[df["Patient_Hash"] != patient_hash]

            if len(filtered_df) < len(df):
                save_ledger(filtered_df)
                st.success(f"🗑️ All records for **{patient_name}** have been deleted.")
            else:
                st.warning(f"No records found for **{patient_name}**.")
        else:
            st.error("⚠️ Please enter a valid patient name.")

# Streamlit UI Layout
st.title("🔗 Secure Blockchain-Based Hospital Ledger")
st.markdown("A **secure and efficient hospital ledger system** using hashing and blockchain-like transactions.")

# Sidebar for navigation
menu = st.sidebar.radio("Navigation", ["Add Patient Visit", "Search Patient", "Retrieve Full Ledger", "Delete Patient Record"])

if menu == "Add Patient Visit":
    add_patient_visit()
elif menu == "Search Patient":
    search_patient_visits()
elif menu == "Retrieve Full Ledger":
    retrieve_all_records()
elif menu == "Delete Patient Record":
    delete_patient_record()
