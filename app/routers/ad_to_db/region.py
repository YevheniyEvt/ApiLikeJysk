from fastapi import APIRouter, status, Path, HTTPException
from sqlmodel import select
from typing import Annotated

from app.database import SessionDep
from app.models import Region
from app.schemas import RegionAdd, RegionPublic, RegionUpdate



router = APIRouter(
    prefix="/region",
    tags=["Region"]
)


@router.post("/", response_model=RegionPublic, status_code=status.HTTP_201_CREATED)
def add_region(region: RegionAdd, session: SessionDep):
    db_region = Region.model_validate(region)
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region


@router.get("/", response_model=list[RegionPublic])
def get_regions(session: SessionDep):
    region = session.exec(select(Region)).all()
    return region

@router.get("/{id}", response_model=list[RegionPublic])
def get_region(id: Annotated[int, Path()], session: SessionDep):
    region =  session.get(Region, id)
    if not region:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"district with {id} nor found")
    return region

@router.put("/{id}", response_model=RegionPublic)
def update_region(id: Annotated[int, Path()], region: RegionUpdate, session: SessionDep):
    db_region = session.get(Region, id)
    if not db_region:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"region with {id} nor found")

    region_data = region.model_dump(exclude_unset=True)
    db_region.sqlmodel_update(region_data)
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_region(id: Annotated[int, Path()], session: SessionDep):
    db_region = session.get(Region, id)
    if not db_region:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"region with {id} nor found")
    session.delete(db_region)
    session.commit()