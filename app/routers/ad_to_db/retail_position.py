from fastapi import APIRouter, status, Path, HTTPException
from fastapi.params import Query
from sqlmodel import select
from typing import Annotated

from app.database import SessionDep
from app.models import RetailPosition
from app.schemas import RetailPositionAdd, RetailPositionPublic, RetailPositionUpdate



router = APIRouter(
    prefix="/retailposition",
    tags=["Retail Position"]
)


@router.post("/", response_model=RetailPositionPublic, status_code=status.HTTP_201_CREATED)
def add_retail_position(retail_position: RetailPositionAdd, session: SessionDep):
    db_retail_position = RetailPosition.model_validate(retail_position)
    session.add(db_retail_position)
    session.commit()
    session.refresh(db_retail_position)
    return db_retail_position


@router.get("/all", response_model=list[RetailPositionPublic])
def get_retail_positions(session: SessionDep):
    retail_positions = session.exec(select(RetailPosition)).all()
    return retail_positions

@router.get("/", response_model=list[RetailPositionPublic])
def get_retail_position(q: Annotated[str, Query()], session: SessionDep):
    retail_positions = session.exec(select(RetailPosition).where(RetailPosition.short_name == q)).first()
    return retail_positions


@router.put("/", response_model=RetailPositionPublic)
def update_retail_position(q: Annotated[str, Query()], retail_position: RetailPositionUpdate, session: SessionDep):
    db_retail_position = session.exec(select(RetailPosition).where(RetailPosition.short_name == q)).first()
    if not db_retail_position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"retail_position with name {q} nor found")

    location_data = retail_position.model_dump(exclude_unset=True)
    db_retail_position.sqlmodel_update(location_data)
    session.add(db_retail_position)
    session.commit()
    session.refresh(db_retail_position)
    return db_retail_position


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_retail_position(q: Annotated[str, Query()], session: SessionDep):
    db_retail_position = session.exec(select(RetailPosition).where(RetailPosition.short_name == q)).first()
    if not db_retail_position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"retail_position with name {q} nor found")
    session.delete(db_retail_position)
    session.commit()