from datetime import date
from pydantic import BaseModel, EmailStr, Field

class ContactBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=3, max_length=30)
    birthday: date
    additional_info: str | None = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=3, max_length=30)
    birthday: date | None = None
    additional_info: str | None = None

class ContactRead(ContactBase):
    id: int
    class Config:
        from_attributes = True
