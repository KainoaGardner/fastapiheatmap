from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from .database import schemas
from .functions import entries, heatmaps
from .database.database import get_db
from .functions.authentication import user_dependency

router = APIRouter(prefix="/entry", tags=["Date Entries"])


@router.get("/check_today/{heatmap_id}/{date}", response_model=schemas.HeatmapEntry)
def check_today(
    user_auth: user_dependency,
    heatmap_id: int,
    date: date,
    db: Session = Depends(get_db),
):
    user_id = user_auth["id"]
    db_entry = entries.check_today(db, user_id, heatmap_id, date)
    if not db_entry:
        raise HTTPException(status_code=400, detail="Not Finished")
    return db_entry


@router.get("/all_entries/{heatmap_id}", response_model=list[schemas.HeatmapEntry])
def get_all_entries(
    user_auth: user_dependency, heatmap_id: int, db: Session = Depends(get_db)
):
    user_id = user_auth["id"]
    db_heatmap = heatmaps.get_user_heatmap(db, user_id, heatmap_id)
    if not db_heatmap:
        raise HTTPException(status_code=404, detail="Heatmap not found")
    return entries.get_all_entries(db_heatmap)


@router.delete("/remove_today/{heatmap_id}", response_model=schemas.HeatmapEntry)
def remove_today(
    user_auth: user_dependency,
    heatmap_id: int,
    date: schemas.HeatmapEntryDate,
    db: Session = Depends(get_db),
):

    user_id = user_auth["id"]
    db_entry = entries.check_today(db, user_id, heatmap_id, date.date)
    if not db_entry:
        raise HTTPException(status_code=400, detail="Not Finished")
    return entries.remove_today(db, db_entry)


@router.post("/create/{heatmap_id}", response_model=schemas.HeatmapEntry)
def create_entry(
    user_auth: user_dependency,
    heatmap_id: int,
    new_entry: schemas.HeatmapEntryCreate,
    db: Session = Depends(get_db),
):

    user_id = user_auth["id"]
    db_entry = entries.check_today(db, user_id, heatmap_id, new_entry.date)
    if db_entry:
        raise HTTPException(status_code=400, detail="Already Finished")

    return entries.create_entry(db, heatmap_id, new_entry)
