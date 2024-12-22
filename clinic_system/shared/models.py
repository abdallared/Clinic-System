# shared/models.py
import json
from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class Doctor:
    id: str
    name: str
    specialization: str
    contact: str
    schedule: List[str]
    emergency_contact: str = ""
    next: Optional['Doctor'] = None

@dataclass
class Patient:
    id: str
    name: str
    age: int
    gender: str
    contact: str
    medical_history: List[dict]
    assigned_doctor: str = ""
    emergency_contact: str = ""
    notes: str = ""
    next: Optional['Patient'] = None

class DoctorList:
    def __init__(self):
        self.head = None
        self.load_data()

    def add_doctor(self, doctor_data: Dict):
        """Add a new doctor to the list"""
        if isinstance(doctor_data, dict):
            doctor = Doctor(
                id=doctor_data['id'],
                name=doctor_data['name'],
                specialization=doctor_data['specialization'],
                contact=doctor_data['contact'],
                schedule=doctor_data['schedule'],
                emergency_contact=doctor_data.get('emergency_contact', '')
            )
        else:
            doctor = doctor_data

        if not self.head:
            self.head = doctor
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = doctor
        self.save_data()

    def remove_doctor(self, doctor_id: str) -> bool:
        """Remove a doctor from the list"""
        if not self.head:
            return False

        if self.head.id == doctor_id:
            self.head = self.head.next
            self.save_data()
            return True

        current = self.head
        while current.next:
            if current.next.id == doctor_id:
                current.next = current.next.next
                self.save_data()
                return True
            current = current.next
        return False

    def update_doctor(self, doctor_id: str, updated_data: Dict) -> bool:
        """Update doctor information"""
        current = self.head
        while current:
            if current.id == doctor_id:
                for key, value in updated_data.items():
                    if hasattr(current, key):
                        setattr(current, key, value)
                self.save_data()
                return True
            current = current.next
        return False

    def get_all_doctors(self) -> List[Doctor]:
        """Get all doctors in the list"""
        doctors = []
        current = self.head
        while current:
            doctors.append(current)
            current = current.next
        return doctors

    def find_doctor(self, doctor_id: str) -> Optional[Doctor]:
        """Find a doctor by ID"""
        current = self.head
        while current:
            if current.id == doctor_id:
                return current
            current = current.next
        return None

    def save_data(self):
        """Save doctors data to JSON file"""
        data = []
        current = self.head
        while current:
            doctor_dict = {
                'id': current.id,
                'name': current.name,
                'specialization': current.specialization,
                'contact': current.contact,
                'schedule': current.schedule,
                'emergency_contact': current.emergency_contact
            }
            data.append(doctor_dict)
            current = current.next
        
        with open('doctors.json', 'w') as f:
            json.dump(data, f)

    def load_data(self):
        """Load doctors data from JSON file"""
        try:
            with open('doctors.json', 'r') as f:
                data = json.load(f)
                self.head = None  # Reset the list
                for doctor_dict in data:
                    self.add_doctor(doctor_dict)
        except FileNotFoundError:
            pass

class PatientList:
    def __init__(self):
        self.head = None
        self.load_data()

    def add_patient(self, patient_data: Dict):
        """Add a new patient to the list"""
        if isinstance(patient_data, dict):
            patient = Patient(
                id=patient_data['id'],
                name=patient_data['name'],
                age=patient_data['age'],
                gender=patient_data['gender'],
                contact=patient_data['contact'],
                medical_history=patient_data.get('medical_history', []),
                assigned_doctor=patient_data.get('assigned_doctor', ''),
                emergency_contact=patient_data.get('emergency_contact', ''),
                notes=patient_data.get('notes', '')
            )
        else:
            patient = patient_data

        if not self.head:
            self.head = patient
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = patient
        self.save_data()

    def remove_patient(self, patient_id: str) -> bool:
        """Remove a patient from the list"""
        if not self.head:
            return False

        if self.head.id == patient_id:
            self.head = self.head.next
            self.save_data()
            return True

        current = self.head
        while current.next:
            if current.next.id == patient_id:
                current.next = current.next.next
                self.save_data()
                return True
            current = current.next
        return False

    def update_patient(self, patient_id: str, updated_data: Dict) -> bool:
        """Update patient information"""
        current = self.head
        while current:
            if current.id == patient_id:
                for key, value in updated_data.items():
                    if hasattr(current, key):
                        setattr(current, key, value)
                self.save_data()
                return True
            current = current.next
        return False

    def get_all_patients(self) -> List[Patient]:
        """Get all patients in the list"""
        patients = []
        current = self.head
        while current:
            patients.append(current)
            current = current.next
        return patients

    def find_patient(self, patient_id: str) -> Optional[Patient]:
        """Find a patient by ID"""
        current = self.head
        while current:
            if current.id == patient_id:
                return current
            current = current.next
        return None

    def search_patients(self, search_term: str) -> List[Patient]:
        """Search patients by various criteria"""
        results = []
        current = self.head
        search_term = search_term.lower()
        
        while current:
            # Search in multiple fields
            if (search_term in current.name.lower() or
                search_term in current.id.lower() or
                search_term in current.contact.lower() or
                search_term in str(current.age) or
                search_term in current.assigned_doctor.lower()):
                results.append(current)
            current = current.next
        return results

    def add_medical_record(self, patient_id: str, record: Dict) -> bool:
        """Add a medical record to a patient's history"""
        patient = self.find_patient(patient_id)
        if patient:
            patient.medical_history.append(record)
            self.save_data()
            return True
        return False

    def save_data(self):
        """Save patients data to JSON file"""
        data = []
        current = self.head
        while current:
            patient_dict = {
                'id': current.id,
                'name': current.name,
                'age': current.age,
                'gender': current.gender,
                'contact': current.contact,
                'medical_history': current.medical_history,
                'assigned_doctor': current.assigned_doctor,
                'emergency_contact': current.emergency_contact,
                'notes': current.notes
            }
            data.append(patient_dict)
            current = current.next
        
        with open('patients.json', 'w') as f:
            json.dump(data, f)

    def load_data(self):
        """Load patients data from JSON file"""
        try:
            with open('patients.json', 'r') as f:
                data = json.load(f)
                self.head = None  # Reset the list
                for patient_dict in data:
                    self.add_patient(patient_dict)
        except FileNotFoundError:
            pass