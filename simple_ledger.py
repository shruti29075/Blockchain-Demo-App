import streamlit as st
import pandas as pd
import hashlib
import os

# File name for CSV storage
CSV_FILE = "hospital_ledger.csv"

# Function to generate hash (for patient names)
def generate_hash(patient_name):
    return hashlib.sha256(patient_name.encode()).hexdigest()

# Function to load the hospital ledger
def load_ledger():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Patient_Hash", "Treatment", "Cost", "Date_of_Visit"])

# Function to save the hospital ledger
def save_ledger(df):
    df.to_csv(CSV_FILE, index=False)

# Function to add a new patient visit
def add_patient_visit():
    st.subheader("Add Patient Visit")
    patient_name = st.text_input("Enter Patient's Name:")
    treatment = st.text_input("Enter Treatment Received:")
    cost = st.number_input("Enter Cost ($):", min_value=0.0, format="%.2f")
    date_of_visit = st.date_input("Select Date of Visit")

    if st.button("Add Visit"):
        if patient_name and treatment and cost:
            df = load_ledger()
            patient_hash = generate_hash(patient_name)

            new_entry = pd.DataFrame(
                [[patient_hash, treatment, cost, date_of_visit]],
                columns=["Patient_Hash", "Treatment", "Cost", "Date_of_Visit"]
            )

            df = pd.concat([df, new_entry], ignore_index=True)
            save_ledger(df)
            st.success(f"Visit added for {patient_name} (Stored as Hash: {patient_hash})")
        else:
            st.error("Please fill all fields before adding a visit.")

# Function to search for a patient's visits
def search_patient_visits():
    st.subheader("Search Patient Records")
    patient_name = st.text_input("Enter Patient's Name to Search:")
    
    if st.button("Search"):
        df = load_ledger()
        if patient_name:
            patient_hash = generate_hash(patient_name)
            filtered_df = df[df["Patient_Hash"] == patient_hash]

            if not filtered_df.empty:
                st.write(f"Records for {patient_name}:")
                st.dataframe(filtered_df)
            else:
                st.warning(f"No records found for {patient_name}.")
        else:
            st.error("Please enter a patient name.")

# Function to display all records
def retrieve_all_records():
    st.subheader("Retrieve Full Ledger")
    df = load_ledger()
    
    if df.empty:
        st.warning("No records found in the ledger.")
    else:
        st.write("Complete Hospital Ledger:")
        st.dataframe(df)

# Function to delete a patient's records
def delete_patient_record():
    st.subheader("Delete Patient Records")
    patient_name = st.text_input("Enter Patient's Name to Delete:")

    if st.button("Delete"):
        df = load_ledger()
        if patient_name:
            patient_hash = generate_hash(patient_name)
            filtered_df = df[df["Patient_Hash"] != patient_hash]

            if len(filtered_df) < len(df):
                save_ledger(filtered_df)
                st.success(f"All records for {patient_name} have been deleted.")
            else:
                st.warning(f"No records found for {patient_name}.")
        else:
            st.error("Please enter a patient name.")

# Streamlit UI Layout
st.title("🔗 Secure Blockchain-Based Hospital Ledger")
st.markdown("A **simple, secure, and efficient hospital ledger system** using hashing and CSV storage.")

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
