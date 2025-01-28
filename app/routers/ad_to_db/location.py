from fastapi import APIRouter, status, Depends, Path, HTTPException
from sqlmodel import select
from typing import Annotated

from app.database import SessionDep
from app.models import Location
from app.schemas import LocationAdd, LocationPublic, LocationUpdate



router = APIRouter(
    prefix="/location",
    tags=["Location"]
)


@router.post("/", response_model=LocationPublic, status_code=status.HTTP_201_CREATED)
def add_location(location: LocationAdd, session: SessionDep):
    db_location = Location.model_validate(location)
    session.add(db_location)
    session.commit()
    session.refresh(db_location)
    return db_location


@router.get("/", response_model=list[LocationPublic])
def get_locations(session: SessionDep):
    locations = session.exec(select(Location)).all()
    return locations


@router.put("/{id}", response_model=LocationPublic)
def update_location(id: Annotated[int, Path()], location: LocationUpdate, session: SessionDep):
    db_location = session.get(Location, id)
    if not db_location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"location with {id} nor found")

    location_data = location.model_dump(exclude_unset=True)
    db_location.sqlmodel_update(location_data)
    session.add(db_location)
    session.commit()
    session.refresh(db_location)
    return db_location


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(id: Annotated[int, Path()], session: SessionDep):
    db_location = session.get(Location, id)
    if not db_location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"location with {id} nor found")
    session.delete(db_location)
    session.commit()