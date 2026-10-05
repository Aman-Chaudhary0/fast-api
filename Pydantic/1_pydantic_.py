from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Optional,Dict, Annotated

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Nitish', 'Amit'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]

def update_patient_info(patient:Patient):

    print(f"Patient Name: {patient.name}")
    print(f"Patient Email: {patient.email}")
    print(f"Patient Age: {patient.age}")
    print(f"Patient Weight: {patient.weight}")
    print(f"Patient Married: {patient.married}")
    print(f"Patient Allergies: {patient.allergies}")
    print(f"Patient Contact Details: {patient.contact_details}")
    print('update_patient_info function executed successfully!')

patient_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "linkedin_url": "https://www.linkedin.com/in/johndoe",
    "age": 30,
    "weight": 75.5,
    "married": True,
    "allergies": ["Peanuts", "Shellfish"],
    "contact_details": {'phone': '123-456-7890', 'address': '123 Main St, Anytown, USA'}
}

patient1 = Patient(**patient_data)
update_patient_info(patient1)
