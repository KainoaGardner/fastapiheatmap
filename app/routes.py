from fastapi import HTTPException, status, APIRouter

from app import app
from . import users, heatmaps, entries, authentication
from .database.database import get_db

app.include_router(users.router)
app.include_router(heatmaps.router)
app.include_router(entries.router)
app.include_router(authentication.router)
