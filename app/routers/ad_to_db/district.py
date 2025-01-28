from fastapi import APIRouter, status, Path, HTTPException
from sqlmodel import select
from typing import Annotated

from app.database import SessionDep
from app.models import District
from app.schemas import DistrictAdd, DistrictPublic, DistrictUpdate



router = APIRouter(
    prefix="/district",
    tags=["District"]
)


@router.post("/", response_model=DistrictPublic, status_code=status.HTTP_201_CREATED)
def add_district(district: DistrictAdd, session: SessionDep):
    db_district = District.model_validate(district)
    session.add(db_district)
    session.commit()
    session.refresh(db_district)
    return db_district


@router.get("/", response_model=list[DistrictPublic])
def get_districts(session: SessionDep):
    district = session.exec(select(District)).all()
    return district

@router.get("/{id}", response_model=list[DistrictPublic])
def get_district(id: Annotated[int, Path()], session: SessionDep):
    district =  session.get(District, id)
    if not district:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"district with {id} nor found")
    return district


@router.put("/{id}", response_model=DistrictPublic)
def update_district(id: Annotated[int, Path()], district: DistrictUpdate, session: SessionDep):
    db_district = session.get(District, id)
    if not db_district:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"district with {id} nor found")

    district_data = district.model_dump(exclude_unset=True)
    db_district.sqlmodel_update(district_data)
    session.add(db_district)
    session.commit()
    session.refresh(db_district)
    return db_district


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_district(id: Annotated[int, Path()], session: SessionDep):
    db_district = session.get(District, id)
    if not db_district:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"district with {id} nor found")
    session.delete(db_district)
    session.commit()