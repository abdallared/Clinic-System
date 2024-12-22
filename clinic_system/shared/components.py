# shared/components.py
import streamlit as st
import pandas as pd

def render_stats_cards(title, value, icon):
    st.markdown(f"""
        <div class="stats-card">
            <div style="font-size: 1.2rem; color: #666;">{icon} {title}</div>
            <div class="big-number">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def render_doctor_table(doctors):
    if isinstance(doctors, list):
        df = pd.DataFrame([{
            'ID': d.id,
            'Name': d.name,
            'Specialization': d.specialization,
            'Contact': d.contact,
            'Schedule': ', '.join(d.schedule)
        } for d in doctors])
    else:
        df = pd.DataFrame([{
            'ID': doctors.id,
            'Name': doctors.name,
            'Specialization': doctors.specialization,
            'Contact': doctors.contact,
            'Schedule': ', '.join(doctors.schedule)
        }])
    
    st.dataframe(df, use_container_width=True)

def render_patient_record(patient):
    with st.container():
        st.markdown(f"""
            <div class="patient-card">
                <h3>{patient.name} (ID: {patient.id})</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("📊 Basic Information")
            st.write(f"Age: {patient.age}")
            st.write(f"Gender: {patient.gender}")
        with col2:
            st.write("📞 Contact Details")
            st.write(f"Contact: {patient.contact}")
            st.write(f"Emergency: {patient.emergency_contact}")
        with col3:
            st.write("👨‍⚕️ Medical Care")
            st.write(f"Assigned Doctor: {patient.assigned_doctor}")
            
        with st.expander("Medical History"):
            if patient.medical_history:
                for record in patient.medical_history:
                    st.markdown(f"""
                        <div class="medical-history">
                            <p><strong>Date:</strong> {record['date']}</p>
                            <p><strong>Diagnosis:</strong> {record['diagnosis']}</p>
                            <p><strong>Prescription:</strong> {record['prescription']}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No medical history available.")

def render_patient_table(patients):
    df = pd.DataFrame([{
        'ID': p.id,
        'Name': p.name,
        'Age': p.age,
        'Gender': p.gender,
        'Contact': p.contact,
        'Doctor': p.assigned_doctor
    } for p in patients])
    
    st.dataframe(df, use_container_width=True)