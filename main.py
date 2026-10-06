from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field,computed_field
from typing import Annotated, Literal,Optional

app = FastAPI()

# Define a Pydantic model for the patient data
class Patient(BaseModel):

    id: Annotated[str, Field(..., description="The ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="The city of the patient", example="New York")]
    age: Annotated[int, Field(...,gt=0,lt=120, description="The age of the patient", example=30)]
    gender: Annotated[Literal["Male", "Female"], Field(..., description="The gender of the patient", example="Male")]
    height: Annotated[float, Field(...,gt=0, description="The height of the patient in meters", example=1.75)]
    weight: Annotated[float, Field(...,gt=0, description="The weight of the patient in kilograms", example=70.5)]


    # Define computed fields for BMI and verdict
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi


    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"



# Define a Pydantic model for updating patient data
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]



# Load your data here (e.g., from a database or a file)
def load_data():
    with open("patients.json", "r") as file:
        data =  json.load(file)
    return data


# Save your data here (e.g., to a database or a file)
def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file)

# Define your API endpoints here
@app.get("/")
def hello():
    return {"message": "Patient Management System API "}


# Get information about the API
@app.get("/about")
def about():
    return {"message": "A fully functional Patient Management System API built with FastAPI."}



# Get all patients
@app.get("/view")
def view_patients():
    data = load_data()
    return data



# Get a specific patient by ID
@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", examples="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")



# Sort patients by height, weight, or BMI
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="sort on the basis of height, weight and bmi"), order: str = Query("asc", description="Order of sorting: 'asc' for ascending, 'desc' for descending")):
    data = load_data()
    valid_sort_keys = ["height", "weight", "bmi"]

    if sort_by not in valid_sort_keys:
        raise HTTPException(status_code=400, detail=f"Invalid sort key. Valid options are: {', '.join(valid_sort_keys)}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Valid options are: 'asc' or 'desc'")

    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == "desc"))
    return sorted_data


# Create a new patient
@app.post("/create")
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    # check if patient with the same ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    #add the new patient to the data
    data[patient.id] = patient.model_dump(exclude=["id"])

    #save the updated data
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient_id": patient.id})



# Update an existing patient
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    # check if the patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    # update the existing patient info with the new values
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # add the patient id to the dict so that we can create a pydantic object
    existing_patient_info['id'] = patient_id

    # create a pydantic object from the updated dict
    patient_pydandic_obj = Patient(**existing_patient_info)

    # remove the id from the dict so that we can save it to the json file
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # update the data with the updated patient info
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})



# Delete a patient
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})

