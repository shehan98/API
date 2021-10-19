from typing import Optional
import uvicorn #ASGI
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

employees = {
    1: {
        "name": "Shehan",
        "age": 23,
        "location": "Tangalle"
    },
    2: {
        "name": "Pasindu",
        "age": 25,
        "location": "Matara"
    },
    3: {
        "name": "Yasindu",
        "age": 34,
        "location": "Galle"
    },
}

class Employee(BaseModel):
    name: str
    age: int
    location: str

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = None


# GET Methods
@app.get('/')
def index():
    return { 'message': 'Welcome'}

@app.get('/home')
def get_name(name: str):
    return {'Hi, i am': f'{name}'}

@app.get('/get-employee/{employee_id}')
def get_employee(employee_id: int = Path(None, description="The ID of the employee ou want to view", gt=0, lt=5)):
    return employees[employee_id]

@app.get('/get-by-name')
def get_employee(name: str):
    for employee_id in employees:
        if employees[employee_id]["name"] == name:
            return employees[employee_id]
    return {"Data": "Not found"}

@app.get('/all-employees')
def get_all_employees():
    return employees

# POST Method
@app.post('/create-employee/{employee_id}')
def create_employee(employee_id : int, employee : Employee):
    if employee_id in employees:
        return {"Error": "This employee exists"}
    
    employees[employee_id] = employee
    return employees[employee_id]


# PUT Method
@app.put('/update-employee/{employee_id}')
def update_employee(employee_id: int, employee: UpdateEmployee):
    if employee_id not in employees:
        return {"Error": "This Employee does not exist"}
    
    if employee.name != None:
        employees[employee_id].name = employee.name

    if employee.age != None:
        employees[employee_id].age = employee.age

    if employee.location != None:
        employees[employee_id].location = employee.location
    
    return employees[employee_id]


# DELETE Method
@app.delete('/delete-employee/{employee_id}')
def delete_employee(employee_id: int):
    if employee_id not in employees:
        return {"Error": "This Employee does not exist"}
    
    del employees[employee_id]
    return {"Message": " Employee deleted successfully"}


# Run the API with uvicorn
if __name__== '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

#uvicorn main:app --reload