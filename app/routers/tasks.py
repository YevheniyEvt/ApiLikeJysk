from fastapi import APIRouter, status, Path, HTTPException, Depends
from sqlmodel import select
from typing import Annotated

from ..database import SessionDep
from ..models import Task, Employee, Location, OfficeDepartment, Store, StorePosition, RetailPosition, District
from ..schemas import TaskAdd, TaskPublic, StorePublicWithEmployee, DistrictPublicWithStores
from ..dependencies import get_current_user



router = APIRouter(
    prefix="/task",
    tags=["Task"]
)


@router.post("/add", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def add_task(current_user: Annotated[Employee, Depends(get_current_user)],
              task: TaskAdd, session: SessionDep):
    extra_data = {}
    if current_user.store_position_name:
        store = session.exec(select(Store).where(Store.id == current_user.store_id)).first()
        position_id = current_user.store_position_name
        position = session.get(StorePosition, position_id)
        location = session.get(Location, position.location_id)
        extra_data = {"owner_id": current_user.id, "location_id": location.id, "department": store.name}

    elif current_user.retail_position_name:
        retail_position = session.exec(select(RetailPosition).where(RetailPosition.id == current_user.retail_position_name)).first()
        location = session.get(Location, retail_position.id)
        district = session.exec(select(District).where(current_user.id == District.district_manager_id)).first()
        extra_data = {"owner_id": current_user.id, "location_id": location.id, "department": district.name}

    elif current_user.office_department:
        office_position = session.exec(select(OfficeDepartment).where(OfficeDepartment.id == current_user.office_department_name)).first()
        location = session.get(Location, office_position.id)
        extra_data = {"owner_id": current_user.id, "location_id": location.id, "department": office_position.position}

    db_task = Task.model_validate(task, update=extra_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/add",
            description="Data, choose to create task")
def data_for_task(current_user: Annotated[Employee, Depends(get_current_user)],  session: SessionDep):
    if current_user.store_position_name:
        store = session.exec(select(Store).where(Store.id == current_user.store_id)).first()
        return StorePublicWithEmployee.model_validate(store)

    if current_user.retail_position_name or current_user.office_department_name:
        districts = session.exec(select(District)).all()
        list_of_districts = []
        for district in districts:
            list_of_districts.append(DistrictPublicWithStores.model_validate(district))
        return list_of_districts

@router.get("/", response_model=list[TaskPublic])
def get_my_task(current_user: Annotated[Employee, Depends(get_current_user)],
              session: SessionDep):
    task = session.exec(select(Task).where(Task.task_recipient_id == current_user.id)).all()
    return task

@router.get("/department", response_model=list[TaskPublic])
def get_my_department_task(current_user: Annotated[Employee, Depends(get_current_user)],
              session: SessionDep):

    if current_user.store_position_name:
        task = []
        store = session.exec(select(Store).where(current_user.store_id == Store.id)).first()
        for employee in store.employee:
            task = session.exec(select(Task).where(Task.task_recipient_id == employee.id)).all()
            task.extend(task)
        return task

    if current_user.retail_position_name:
        district = session.exec(select(District).where(District.district_manager_id == current_user.id)).first()
        task = session.exec(select(Task).where(Task.department == district.name)).all()
        return task

    elif current_user.office_department:
        user_department = session.get(OfficeDepartment, current_user.office_department_name)
        task = session.exec(select(Task).where(Task.department == user_department.position)).all()
        return task


@router.get("/{id}", response_model=TaskPublic)
def get_task(current_user: Annotated[Employee, Depends(get_current_user)],
             id: Annotated[int, Path()], session: SessionDep):
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with {id} nor found")

    return task



