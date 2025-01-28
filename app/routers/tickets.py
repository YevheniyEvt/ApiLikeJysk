from fastapi import APIRouter, status, Path, HTTPException, Depends
from sqlmodel import select
from typing import Annotated

from ..database import SessionDep
from ..models import Ticket, Employee, Location, OfficeDepartment, Store
from ..schemas import TicketAdd, TicketPublic, LocationsForTicket
from ..dependencies import get_current_user



router = APIRouter(
    prefix="/tickets",
    tags=["Ticket"]
)


@router.post("/add", response_model=TicketPublic, status_code=status.HTTP_201_CREATED)
def add_ticket(current_user: Annotated[Employee, Depends(get_current_user)],
              ticket: TicketAdd, session: SessionDep):
    location = session.exec(select(Location).where(Location.name == ticket.location_name)).first()
    if location:
        location_id = location.id
        location_name = location.name
    else:
        location = session.exec(select(OfficeDepartment).where(OfficeDepartment.position == ticket.location_name)).first()
        location_id = location.location_id
        location_name = location.position

    extra_data = {"owner_id": current_user.id, "location_id": location_id, "department":location_name}
    db_ticket = Ticket.model_validate(ticket, update=extra_data)
    session.add(db_ticket)
    session.commit()
    session.refresh(db_ticket)
    return db_ticket


@router.get("/add", response_model=LocationsForTicket,
            description="Location`s name, choose to create ticket")
def location_name_for_ticket(current_user: Annotated[Employee, Depends(get_current_user)],  session: SessionDep):
    location_name = []
    retail_info = session.exec(select(Location).where(Location.name == "Retail")).all()
    for retail in retail_info:
        location_name.append(retail.name)
    office_info = session.exec(select(OfficeDepartment)).all()
    for office in office_info:
        location_name.append(office.position)

    return {'names': location_name}


@router.get("/", response_model=list[TicketPublic])
def get_my_tickets(current_user: Annotated[Employee, Depends(get_current_user)],
              session: SessionDep):
    tickets = session.exec(select(Ticket).where(Ticket.owner_id == current_user.id)).all()
    return tickets

@router.get("/department", response_model=list[TicketPublic])
def get_my_department_tickets(current_user: Annotated[Employee, Depends(get_current_user)],
              session: SessionDep):

    if current_user.store_position_name:
        tickets = []
        store = session.exec(select(Store).where(current_user.store_id == Store.id)).first()
        for employee in store.employee:
            ticket = session.exec(select(Ticket).where(Ticket.owner_id == employee.id)).all()
            tickets.extend(ticket)
        return tickets

    if current_user.retail_position_name:
        tickets = session.exec(select(Ticket).where(Ticket.department == "Retail"))
        return tickets

    elif current_user.office_department:
        user_department = session.get(OfficeDepartment, current_user.office_department_name)
        tickets = session.exec(select(Ticket).where(Ticket.department == user_department.position)).all()
        return tickets


@router.get("/{id}", response_model=TicketPublic)
def get_ticket(current_user: Annotated[Employee, Depends(get_current_user)],
             id: Annotated[int, Path()], session: SessionDep):
    ticket = session.get(Ticket, id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tickets with {id} nor found")
    if ticket.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    return ticket



