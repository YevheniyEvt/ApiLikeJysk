from fastapi import APIRouter, status, Path, HTTPException
from sqlmodel import select
from typing import Annotated

from app.database import SessionDep
from app.models import Employee
from app.schemas import EmployeeAdd, EmployeePublic, EmployeeUpdate



router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


@router.post("/",  status_code=status.HTTP_201_CREATED)
def add_employee(employee: EmployeeAdd, session: SessionDep):
    db_employee = Employee.model_validate(employee)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


@router.get("/", response_model=list[EmployeePublic])
def get_employees(session: SessionDep):
    employee = session.exec(select(Employee)).all()
    return employee


@router.get("/{id}", response_model=EmployeePublic)
def get_employee(id: Annotated[int, Path()], session: SessionDep):
    employee =  session.get(Employee, id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"employee with {id} nor found")
    return employee


@router.put("/{id}", response_model=EmployeePublic)
def update_employee(id: Annotated[int, Path()], employee: EmployeeUpdate, session: SessionDep):
    db_employee = session.get(Employee, id)
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"employee with {id} nor found")

    employee_data = employee.model_dump(exclude_unset=True)
    db_employee.sqlmodel_update(employee_data)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: Annotated[int, Path()], session: SessionDep):
    db_employee = session.get(Employee, id)
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"employee with {id} nor found")
    session.delete(db_employee)
    session.commit()