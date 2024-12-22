import streamlit as st
from shared.models import DoctorList
import pandas as pd
from datetime import datetime, time
import uuid

# Page configuration
st.set_page_config(page_title="Doctor Management", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .doctor-form {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-message {
        color: #28a745;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-message {
        color: #dc3545;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

def validate_phone(phone):
    """Validate phone number format"""
    import re
    pattern = r'^\+?[\d\s-]{10,}$'
    return bool(re.match(pattern, phone))

def delete_doctor(doctor_id):
    """Handle doctor deletion with state management"""
    if 'doctor_list' in st.session_state:
        st.session_state.doctor_list.remove_doctor(doctor_id)
        st.success(f"Doctor with ID {doctor_id} has been deleted")
        st.rerun()

def main():
    st.title("👨‍⚕️ Doctor Management System")

    # Initialize doctor list in session state if not exists
    if 'doctor_list' not in st.session_state:
        st.session_state.doctor_list = DoctorList()

    # Initialize delete confirmation state if not exists
    if 'delete_confirmation' not in st.session_state:
        st.session_state.delete_confirmation = {}

    # Tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Add Doctor", "View Doctors", "Update Doctor"])

    # Add Doctor Tab
    with tab1:
        st.header("Register New Doctor")
        
        with st.form("doctor_registration_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                doctor_id = st.text_input("Doctor ID*", placeholder="Enter unique ID")
                name = st.text_input("Full Name*", placeholder="Dr. First Last")
                specialization = st.selectbox(
                    "Specialization*",
                    ["General Medicine", "Pediatrics", "Cardiology", "Orthopedics", 
                     "Neurology", "Dermatology", "ENT", "Ophthalmology", "Other"]
                )
                if specialization == "Other":
                    specialization = st.text_input("Specify Specialization")
                
                phone = st.text_input("Contact Number*", placeholder="+1234567890")
                
            with col2:
                experience = st.number_input("Years of Experience", min_value=0, max_value=50)
                qualification = st.text_input("Qualifications*", placeholder="MBBS, MD, etc.")
                
                # Working Hours
                st.subheader("Working Hours")
                working_days = st.multiselect(
                    "Working Days*",
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                )
                
                col3, col4 = st.columns(2)
                with col3:
                    start_time = st.time_input("Start Time", time(9, 0))
                with col4:
                    end_time = st.time_input("End Time", time(17, 0))

                emergency_contact = st.text_input("Emergency Contact", placeholder="Emergency contact number")
                
            notes = st.text_area("Additional Notes", placeholder="Any additional information...")
            
            submitted = st.form_submit_button("Register Doctor")
            
            if submitted:
                # Validation
                validation_errors = []
                if not doctor_id or not name or not specialization or not phone:
                    validation_errors.append("Please fill in all required fields marked with *")
                if not validate_phone(phone):
                    validation_errors.append("Please enter a valid phone number")
                if not working_days:
                    validation_errors.append("Please select at least one working day")
                
                if validation_errors:
                    for error in validation_errors:
                        st.error(error)
                else:
                    # Create new doctor
                    new_doctor = {
                        'id': doctor_id,
                        'name': name,
                        'specialization': specialization,
                        'contact': phone,
                        'experience': experience,
                        'qualification': qualification,
                        'schedule': working_days,
                        'working_hours': {
                            'start': start_time.strftime("%H:%M"),
                            'end': end_time.strftime("%H:%M")
                        },
                        'emergency_contact': emergency_contact,
                        'notes': notes
                    }
                    
                    # Add to list
                    st.session_state.doctor_list.add_doctor(new_doctor)
                    st.success("Doctor registered successfully!")
                    st.rerun()

    # View Doctors Tab
    with tab2:
        st.header("Registered Doctors")
        doctors = st.session_state.doctor_list.get_all_doctors()
        
        if doctors:
            for index, doctor in enumerate(doctors):
                try:
                    with st.expander(f"Dr. {doctor.name} ({doctor.specialization})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("*Contact Information*")
                            st.write(f"📞 Phone: {doctor.contact}")
                            if hasattr(doctor, 'emergency_contact'):
                                st.write(f"🚨 Emergency Contact: {doctor.emergency_contact}")
                        
                        with col2:
                            st.write("*Professional Details*")
                            st.write("📅 Working Days: " + ", ".join(doctor.schedule))
                        
                        if hasattr(doctor, 'notes') and doctor.notes:
                            st.write("*Additional Notes*")
                            st.write(doctor.notes)
                        
                        # Two-step deletion process
                        delete_key = f"delete_{doctor.id}_{index}"
                        confirm_key = f"confirm_{doctor.id}_{index}"
                        
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if delete_key not in st.session_state.delete_confirmation:
                                st.session_state.delete_confirmation[delete_key] = False
                            
                            if not st.session_state.delete_confirmation[delete_key]:
                                if st.button("🗑️ Delete", key=delete_key, type="secondary"):
                                    st.session_state.delete_confirmation[delete_key] = True
                                    st.rerun()
                            else:
                                col3, col4 = st.columns(2)
                                with col3:
                                    if st.button("✅ Confirm", key=confirm_key, type="primary"):
                                        delete_doctor(doctor.id)
                                with col4:
                                    if st.button("❌ Cancel", key=f"cancel_{doctor.id}_{index}", type="secondary"):
                                        st.session_state.delete_confirmation[delete_key] = False
                                        st.rerun()
                except Exception as e:
                    st.error(f"Error displaying doctor information: {str(e)}")
        else:
            st.info("No doctors registered yet.")

    # Update Doctor Tab
    with tab3:
        st.header("Update Doctor Information")
        doctors = st.session_state.doctor_list.get_all_doctors()
        
        if doctors:
            doctor_names = [f"Dr. {doctor.name} ({doctor.id})" for doctor in doctors]
            selected_doctor = st.selectbox("Select Doctor to Update", doctor_names)
            
            if selected_doctor:
                doctor_id = selected_doctor.split('(')[-1].strip(')')
                doctor = next((d for d in doctors if d.id == doctor_id), None)
                
                if doctor:
                    with st.form("update_doctor_form"):
                        phone = st.text_input("Update Contact Number", doctor.contact)
                        working_days = st.multiselect(
                            "Update Working Days",
                            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                            default=doctor.schedule
                        )
                        notes = st.text_area("Update Notes", getattr(doctor, 'notes', ''))
                        
                        if st.form_submit_button("Update Information"):
                            updates = {
                                'contact': phone,
                                'schedule': working_days,
                                'notes': notes
                            }
                            st.session_state.doctor_list.update_doctor(doctor_id, updates)
                            st.success("Doctor information updated successfully!")
                            st.rerun()
        else:
            st.info("No doctors available to update.")

if __name__ == "__main__":
    main()