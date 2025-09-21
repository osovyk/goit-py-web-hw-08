from datetime import date, timedelta
from sqlalchemy import select, or_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Contact

async def create_contact(session: AsyncSession, data: dict) -> Contact:
    contact = Contact(**data)
    session.add(contact)
    await session.commit()
    await session.refresh(contact)
    return contact

async def get_contacts(session: AsyncSession, first_name: str | None, last_name: str | None, email: str | None) -> list[Contact]:
    stmt = select(Contact)
    if first_name or last_name or email:
        filters = []
        if first_name:
            filters.append(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            filters.append(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            filters.append(Contact.email.ilike(f"%{email}%"))
        stmt = stmt.where(or_(*filters))
    result = await session.execute(stmt.order_by(Contact.id))
    return list(result.scalars().all())

async def get_contact(session: AsyncSession, contact_id: int) -> Contact | None:
    result = await session.execute(select(Contact).where(Contact.id == contact_id))
    return result.scalars().first()

async def update_contact(session: AsyncSession, contact_id: int, data: dict) -> Contact | None:
    if not data:
        return await get_contact(session, contact_id)
    await session.execute(update(Contact).where(Contact.id == contact_id).values(**data))
    await session.commit()
    return await get_contact(session, contact_id)

async def delete_contact(session: AsyncSession, contact_id: int) -> bool:
    res = await session.execute(delete(Contact).where(Contact.id == contact_id))
    await session.commit()
    return res.rowcount > 0

def _next_7_days_window(today: date) -> list[tuple[int, int]]:
    days = []
    for i in range(0, 7):
        d = today + timedelta(days=i)
        days.append((d.month, d.day))
    return days

async def get_upcoming_birthdays(session: AsyncSession, today: date | None = None) -> list[Contact]:
    base = today or date.today()
    window = _next_7_days_window(base)
    result = await session.execute(select(Contact))
    contacts = result.scalars().all()
    matched = [c for c in contacts if (c.birthday.month, c.birthday.day) in window]
    return matched
