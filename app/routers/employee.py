from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel


router = APIRouter(prefix="/employees",tags=["Employee"])
#PYDANTIC VALIDATION
class EmployeeRequest(BaseModel):
    name:str
    department:str
    salary : float

class EmployeeResponse(BaseModel):
    name:str
    department:str

employee_db={}
employee_id =0

@router.post("/",response_model=EmployeeResponse)
def create_employee(employee:EmployeeRequest):
    global employee_id,employee_db
    employee_id+=1
    employee_db[employee_id]=employee
    return employee

@router.get("/")
def get_employees():
    return employee_db


@router.put("/{employee_id}",response_model=EmployeeResponse)
def update_employee(employee_id:int,employee:EmployeeRequest):
    global employee_db
    if employee_id not in employee_db:
        raise HTTPException(
            status_code =404,
            detail="Employee not found"
        )
    employee_db[employee_id] = employee
    return employee

@router.delete("/{employee_id}")
def delete_employee(employee_id:int):
    global employee_db
    if employee_id not in employee_db:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    del employee_db[employee_id]

    return {
        "message": "Employee deleted successfully"
    }


def connection_DB():
    return {"message":
    "I need a database session."}
@router.get("/db")
def db(connection=Depends(connection_DB)):
    return {
        "database": connection
    }