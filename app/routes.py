from app import app
from . import users, heatmaps, entries, authentication

app.include_router(users.router)
app.include_router(heatmaps.router)
app.include_router(entries.router)
app.include_router(authentication.router)
