from fastapi import APIRouter, status, Path, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from app.database import SessionDep
from app.models import OfficeDepartment
from app.schemas import OfficeDepartmentAdd, OfficeDepartmentPublic, OfficeDepartmentUpdate



router = APIRouter(
    prefix="/officedepartment",
    tags=["Office Department Position"]
)


@router.post("/", response_model=OfficeDepartmentPublic, status_code=status.HTTP_201_CREATED)
def add_office_department(office_department: OfficeDepartmentAdd, session: SessionDep):
    db_office_department = OfficeDepartment.model_validate(office_department)
    session.add(db_office_department)
    session.commit()
    session.refresh(db_office_department)
    return db_office_department


@router.get("/all", response_model=list[OfficeDepartmentPublic])
def get_office_departments(session: SessionDep):
    office_department = session.exec(select(OfficeDepartment)).all()
    return office_department

@router.get("/", response_model=OfficeDepartmentPublic)
def get_office_department(q: Annotated[str, Query()], session: SessionDep):
    office_department = session.exec(select(OfficeDepartment).where(OfficeDepartment.short_name == q)).first()
    return office_department



@router.put("/", response_model=OfficeDepartmentPublic)
def update_office_department(q: Annotated[str, Query()], office_department: OfficeDepartmentUpdate, session: SessionDep):
    db_office_department = session.exec(select(OfficeDepartment).where(OfficeDepartment.short_name == q)).first()
    if not db_office_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"office department with name {q} nor found")

    office_department_data = office_department.model_dump(exclude_unset=True)
    db_office_department.sqlmodel_update(office_department_data)
    session.add(db_office_department)
    session.commit()
    session.refresh(db_office_department)
    return db_office_department


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_office_department(q: Annotated[str, Query()], session: SessionDep):
    db_office_department = session.exec(select(OfficeDepartment).where(OfficeDepartment.short_name == q)).first()
    if not db_office_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"office department with name {q} nor found")
    session.delete(db_office_department)
    session.commit()