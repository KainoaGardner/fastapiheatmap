from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

from .database import schemas
from .functions import entries
from .database.database import get_db

router = APIRouter(prefix="/entry", tags=["Date Entries"])


@router.get("/check_today/{heatmap_id}/{date}", response_model=schemas.HeatmapEntry)
def check_today(
    heatmap_id: int,
    date: str,
    db: Session = Depends(get_db),
):
    db_entry = entries.check_today(db, heatmap_id, date)
    if not db_entry:
        raise HTTPException(status_code=400, detail="Not Finished")
    return db_entry


@router.post("/create/{user_id}/{heatmap_id}", response_model=schemas.HeatmapEntry)
def create_entry(
    user_id: int,
    heatmap_id: int,
    new_entry: schemas.HeatmapEntryCreate,
    db: Session = Depends(get_db),
):
    db_entry = entries.check_today(db, heatmap_id, new_entry.date)
    if db_entry:
        raise HTTPException(status_code=400, detail="Already Finished")

    return entries.create_entry(db, heatmap_id, new_entry)
