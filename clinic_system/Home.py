# Home.py
import streamlit as st
from shared.models import DoctorList, PatientList
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Clinic Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .big-title {
        font-size: 3rem !important;
        color: #1f77b4;
        text-align: center;
        padding: 2rem 0;
    }
    .card {
        border-radius: 10px;
        padding: 1.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .welcome-text {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-section {
        margin-top: 2rem;
        padding: 1rem;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'doctor_list' not in st.session_state:
        st.session_state.doctor_list = DoctorList()
    if 'patient_list' not in st.session_state:
        st.session_state.patient_list = PatientList()

    # Header
    st.markdown('<h1 class="big-title">🏥 Clinic Management System</h1>', unsafe_allow_html=True)
    
    # Welcome message
    current_time = datetime.now()
    greeting = "Good morning" if 5 <= current_time.hour < 12 else \
              "Good afternoon" if 12 <= current_time.hour < 18 else "Good evening"
    
    st.markdown(f'<p class="welcome-text">{greeting}! Welcome to your comprehensive clinic management solution.</p>', 
                unsafe_allow_html=True)

    # Quick Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card">
                <h3>👨‍⚕️ Doctors</h3>
                <div class="stat-number">{}</div>
                <p>Active Healthcare Providers</p>
            </div>
        """.format(len(st.session_state.doctor_list.get_all_doctors())), unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <h3>👥 Patients</h3>
                <div class="stat-number">{}</div>
                <p>Registered Patients</p>
            </div>
        """.format(len(st.session_state.patient_list.get_all_patients())), unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="card">
                <h3>📅 Today</h3>
                <div class="stat-number">{}</div>
                <p>{}</p>
            </div>
        """.format(current_time.strftime("%d"), current_time.strftime("%B %Y")), unsafe_allow_html=True)

    # Quick Access Section
    st.markdown("### 🚀 Quick Access")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="card">
                <h3>📋 Administrative Tasks</h3>
                <ul>
                    <li>Manage doctor schedules</li>
                    <li>View clinic analytics</li>
                    <li>Handle staff records</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to Admin Dashboard", use_container_width=True):
            st.switch_page("pages/1_🏥_Admin_Dashboard.py")

    with col2:
        st.markdown("""
            <div class="card">
                <h3>👥 Patient Care</h3>
                <ul>
                    <li>Register new patients</li>
                    <li>Update medical records</li>
                    <li>Search patient history</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to Patient Management", use_container_width=True):
            st.switch_page("pages/2_👥_Patient_Management.py")

    # System Overview
    st.markdown("### 💡 System Overview")
    st.markdown("""
        <div class="feature-section">
            <p>The Clinic Management System provides a comprehensive solution for healthcare facilities:</p>
            <ul>
                <li><strong>Administrative Dashboard:</strong> Manage staff, view analytics, and handle clinic operations</li>
                <li><strong>Patient Management:</strong> Handle patient records, appointments, and medical histories</li>
                <li><strong>Data Security:</strong> Secure storage and handling of sensitive medical information</li>
                <li><strong>Easy Navigation:</strong> Intuitive interface for both administrative and medical staff</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Support:** For technical assistance, contact IT support")
    with col2:
        st.markdown("**Version:** 1.0.0")
    with col3:
        st.markdown("**Last Updated:** " + current_time.strftime("%Y-%m-%d"))

if __name__ == "__main__":
    main()