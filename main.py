from fastapi import FastAPI,Path,HTTPException,Query
import json
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class Patient(BaseModel):

    id: str
    name: str
    city: str
    age: int
    gender: str
    height: float
    weight: float

# Load data from a JSON file
def load_data():
    # Load your data here (e.g., from a database or a file)
    with open("patients.json", "r") as file:
        data =  json.load(file)
    return data

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
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
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