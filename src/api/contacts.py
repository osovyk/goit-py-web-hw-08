from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.schemas import ContactCreate, ContactRead, ContactUpdate
from src.services.contacts import (
    service_create_contact,
    service_list_contacts,
    service_get_contact,
    service_update_contact,
    service_delete_contact,
    service_upcoming_birthdays,
)

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
async def create_contact(payload: ContactCreate, db: AsyncSession = Depends(get_db)):
    contact = await service_create_contact(db, payload.model_dump())
    return contact

@router.get("/", response_model=list[ContactRead])
async def list_contacts(first_name: str | None = None, last_name: str | None = None, email: str | None = None, db: AsyncSession = Depends(get_db)):
    contacts = await service_list_contacts(db, first_name, last_name, email)
    return contacts

@router.get("/{contact_id}", response_model=ContactRead)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await service_get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact

@router.put("/{contact_id}", response_model=ContactRead)
async def update_contact(contact_id: int, payload: ContactUpdate, db: AsyncSession = Depends(get_db)):
    exists = await service_get_contact(db, contact_id)
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    contact = await service_update_contact(db, contact_id, {k: v for k, v in payload.model_dump(exclude_unset=True).items()})
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    ok = await service_delete_contact(db, contact_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

@router.get("/birthdays/upcoming", response_model=list[ContactRead])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    contacts = await service_upcoming_birthdays(db)
    return contacts
