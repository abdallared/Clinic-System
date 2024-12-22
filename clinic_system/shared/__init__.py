# shared/__init__.py
from .models import Doctor, Patient, DoctorList, PatientList

# Package metadata
__version__ = '1.0.0'
__author__ = 'Clinic Management System'

# Export main classes
__all__ = [
    'Doctor',
    'Patient',
    'DoctorList',
    'PatientList'
]