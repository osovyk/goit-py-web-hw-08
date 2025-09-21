from fastapi import FastAPI
from src.api.contacts import router as contacts_router

app = FastAPI(title="Contacts API")
app.include_router(contacts_router, prefix="/api")
