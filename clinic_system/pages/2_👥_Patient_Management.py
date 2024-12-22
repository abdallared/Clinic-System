# pages/2_👥_Patient_Management.py
import streamlit as st
from shared.models import PatientList, DoctorList
from shared.components import render_patient_record, render_patient_table
import datetime

st.set_page_config(page_title="Patient Management", layout="wide")

# Apply custom CSS
st.markdown("""
    <style>
    .patient-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .search-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .medical-history {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("👥 Patient Management")

    # Initialize session state
    if 'patient_list' not in st.session_state:
        st.session_state.patient_list = PatientList()
    if 'doctor_list' not in st.session_state:
        st.session_state.doctor_list = DoctorList()

    # Tabs for different patient management functions
    tab1, tab2, tab3 = st.tabs(["📝 Register Patient", "🔍 Search Patients", "📋 Patient Records"])

    with tab1:
        st.header("Register New Patient")
        with st.form("add_patient_form"):
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.text_input("Patient ID")
                name = st.text_input("Full Name")
                age = st.number_input("Age", min_value=0, max_value=150)
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                contact = st.text_input("Contact Number")
                doctors = st.session_state.doctor_list.get_all_doctors()
                doctor_options = [""] + [f"{d.name} ({d.specialization})" for d in doctors]
                assigned_doctor = st.selectbox("Assign Doctor", doctor_options)

            emergency_contact = st.text_input("Emergency Contact")
            medical_notes = st.text_area("Medical Notes")

            if st.form_submit_button("Register Patient"):
                if patient_id and name and contact:
                    new_patient = {
                        "id": patient_id,
                        "name": name,
                        "age": age,
                        "gender": gender,
                        "contact": contact,
                        "assigned_doctor": assigned_doctor,
                        "emergency_contact": emergency_contact,
                        "medical_history": [],
                        "notes": medical_notes
                    }
                    st.session_state.patient_list.add_patient(new_patient)
                    st.success("Patient registered successfully!")
                else:
                    st.error("Please fill in all required fields.")

    with tab2:
        st.header("Search Patients")
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search by Name, ID, or Contact Number", 
                                      placeholder="Enter search term...")
        with col2:
            search_by = st.selectbox("Search By", ["All Fields", "Name", "ID", "Contact"])

        if search_term:
            results = st.session_state.patient_list.search_patients(search_term)
            if results:
                st.write(f"Found {len(results)} matching patients:")
                for patient in results:
                    render_patient_record(patient)
            else:
                st.info("No matching patients found.")

    with tab3:
        st.header("All Patient Records")
        patients = st.session_state.patient_list.get_all_patients()
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_doctor = st.selectbox("Filter by Doctor", 
                ["All"] + [d.name for d in st.session_state.doctor_list.get_all_doctors()])
        with col2:
            filter_gender = st.selectbox("Filter by Gender", ["All", "Male", "Female", "Other"])
        with col3:
            sort_by = st.selectbox("Sort by", ["Name", "ID", "Age"])

        if patients:
            # Apply filters
            if filter_doctor != "All":
                patients = [p for p in patients if p.assigned_doctor.startswith(filter_doctor)]
            if filter_gender != "All":
                patients = [p for p in patients if p.gender == filter_gender]

            # Sort patients
            if sort_by == "Name":
                patients.sort(key=lambda x: x.name)
            elif sort_by == "ID":
                patients.sort(key=lambda x: x.id)
            elif sort_by == "Age":
                patients.sort(key=lambda x: x.age)

            for patient in patients:
                render_patient_record(patient)
        else:
            st.info("No patients registered yet.")

if __name__ == "__main__":
    main()