from fastapi import APIRouter, status, Depends, Path, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from app.database import SessionDep
from app.models import StorePosition
from app.schemas import StorePositionUpdate, StorePositionAdd, StorePositionPublic



router = APIRouter(
    prefix="/storeposition",
    tags=["Store Position"]
)


@router.post("/", response_model=StorePositionPublic, status_code=status.HTTP_201_CREATED)
def add_store_position(store_position: StorePositionAdd, session: SessionDep):
    db_store_position = StorePosition.model_validate(store_position)
    session.add(db_store_position)
    session.commit()
    session.refresh(db_store_position)
    return db_store_position


@router.get("/all", response_model=list[StorePositionPublic])
def get_store_positions(session: SessionDep):
    store_position = session.exec(select(StorePosition)).all()
    return store_position


@router.put("/", response_model=StorePositionPublic)
def update_store_position(q: Annotated[str, Query()], store_position: StorePositionUpdate, session: SessionDep):
    db_store_position = session.exec(select(StorePosition).where(StorePosition.short_name == q)).first()
    if not db_store_position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"store position with name {q} nor found")

    store_position_data = store_position.model_dump(exclude_unset=True)
    db_store_position.sqlmodel_update(store_position_data)
    session.add(db_store_position)
    session.commit()
    session.refresh(db_store_position)
    return db_store_position


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_store_position(q: Annotated[str, Query()], session: SessionDep):
    db_store_position = session.exec(select(StorePosition).where(StorePosition.short_name == q)).first()
    if not db_store_position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"store_position with name {q} nor found")
    session.delete(db_store_position)
    session.commit()