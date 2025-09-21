from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import (
    create_contact,
    get_contacts,
    get_contact,
    update_contact,
    delete_contact,
    get_upcoming_birthdays,
)

async def service_create_contact(session: AsyncSession, payload: dict):
    return await create_contact(session, payload)

async def service_list_contacts(session: AsyncSession, first_name: str | None, last_name: str | None, email: str | None):
    return await get_contacts(session, first_name, last_name, email)

async def service_get_contact(session: AsyncSession, contact_id: int):
    return await get_contact(session, contact_id)

async def service_update_contact(session: AsyncSession, contact_id: int, payload: dict):
    return await update_contact(session, contact_id, payload)

async def service_delete_contact(session: AsyncSession, contact_id: int):
    return await delete_contact(session, contact_id)

async def service_upcoming_birthdays(session: AsyncSession, today: date | None = None):
    return await get_upcoming_birthdays(session, today)
