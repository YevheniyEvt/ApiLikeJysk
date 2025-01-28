from fastapi import APIRouter, status, Path, HTTPException
from sqlmodel import select
from typing import Annotated

from app.database import SessionDep
from app.models import Store
from app.schemas import StoreAdd, StorePublic, StoreUpdate



router = APIRouter(
    prefix="/store",
    tags=["Store"]
)


@router.post("/", response_model=StorePublic, status_code=status.HTTP_201_CREATED)
def add_store(store: StoreAdd, session: SessionDep):
    db_store = Store.model_validate(store)
    session.add(db_store)
    session.commit()
    session.refresh(db_store)
    return db_store


@router.get("/", response_model=list[StorePublic])
def get_store(session: SessionDep):
    store = session.exec(select(Store)).all()
    return store


@router.put("/{id}", response_model=StorePublic)
def update_store(id: Annotated[int, Path()], store: StoreUpdate, session: SessionDep):
    db_store = session.get(Store, id)
    if not db_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"store with {id} nor found")

    store_data = store.model_dump(exclude_unset=True)
    db_store.sqlmodel_update(store_data)
    session.add(db_store)
    session.commit()
    session.refresh(db_store)
    return db_store


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(id: Annotated[int, Path()], session: SessionDep):
    db_store = session.get(Store, id)
    if not db_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"store with {id} nor found")
    session.delete(db_store)
    session.commit()