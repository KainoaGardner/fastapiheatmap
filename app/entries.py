from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from .database import schemas
from .functions import entries, heatmaps
from .database.database import get_db
from .functions.authentication import user_dependency


router = APIRouter(prefix="/entry", tags=["Date Entries"])


@router.get("/check_date/{heatmap}/", response_model=schemas.HeatmapEntry)
def check_date(
    user_auth: user_dependency,
    heatmap: str,
    search_by_id: bool = False,
    date: date = date.today(),
    db: Session = Depends(get_db),
):
    user_id = user_auth["id"]
    if search_by_id:
        db_entry = entries.check_today(db, user_id, int(heatmap), date)
    else:
        db_heatmap = heatmaps.get_heatmap_title(db, user_id, heatmap)
        if not db_heatmap:
            raise HTTPException(status_code=404, detail="Heatmap not found")
        db_entry = entries.check_today(db, user_id, db_heatmap.id, date)

    if not db_entry:
        raise HTTPException(status_code=400, detail="Not Finished")
    return db_entry


@router.get("/all_entries/{heatmap}/", response_model=list[schemas.HeatmapEntry])
def get_all_entries(
    user_auth: user_dependency,
    heatmap: str,
    search_by_id: bool = False,
    db: Session = Depends(get_db),
):
    user_id = user_auth["id"]
    if search_by_id:
        db_heatmap = heatmaps.get_user_heatmap(db, user_id, int(heatmap))
    else:
        db_heatmap = heatmaps.get_heatmap_title(db, user_id, heatmap)

    if not db_heatmap:
        raise HTTPException(status_code=404, detail="Heatmap not found")
    return entries.get_all_entries(db_heatmap)


@router.post("/finish_today/{heatmap}/", response_model=schemas.HeatmapEntry)
def finish_today(
    user_auth: user_dependency,
    heatmap: str,
    search_by_id: bool = False,
    date: date = date.today(),
    db: Session = Depends(get_db),
):

    user_id = user_auth["id"]
    if search_by_id:
        db_entry = entries.check_today(db, user_id, int(heatmap), date)
        heatmap_id = int(heatmap)
    else:
        db_heatmap = heatmaps.get_heatmap_title(db, user_id, heatmap)
        if not db_heatmap:
            raise HTTPException(status_code=404, detail="Heatmap not found")
        db_entry = entries.check_today(db, user_id, db_heatmap.id, date)
        heatmap_id = db_heatmap.id

    if db_entry:
        raise HTTPException(status_code=400, detail="Already Finished")

    return entries.create_entry(db, heatmap_id, date)


@router.delete("/unfinish_today/{heatmap}/", response_model=schemas.HeatmapEntry)
def unfinish_today(
    user_auth: user_dependency,
    heatmap: str,
    search_by_id: bool = False,
    date: date = date.today(),
    db: Session = Depends(get_db),
):

    user_id = user_auth["id"]
    if search_by_id:
        db_entry = entries.check_today(db, user_id, int(heatmap), date)
        heatmap_id = int(heatmap)
    else:
        db_heatmap = heatmaps.get_heatmap_title(db, user_id, heatmap)
        if not db_heatmap:
            raise HTTPException(status_code=404, detail="Heatmap not found")
        heatmap_id = db_heatmap.id

    db_entry = entries.check_today(db, user_id, heatmap_id, date)
    if not db_entry:
        raise HTTPException(status_code=400, detail="Not Finished")
    return entries.remove_today(db, db_entry)


# @router.delete(
#     "/unfinish_today/title/{heatmap_title}/", response_model=schemas.HeatmapEntry
# )
# def unfinish_today_title(
#     user_auth: user_dependency,
#     heatmap_title: str,
#     date: schemas.HeatmapEntryDate,
#     db: Session = Depends(get_db),
# ):
#
#     user_id = user_auth["id"]
#     db_heatmap = heatmaps.get_heatmap_title(db, user_id, heatmap_title)
#     if not db_heatmap:
#         raise HTTPException(status_code=404, detail="Heatmap not found")
#
#     db_entry = entries.check_today(db, user_id, db_heatmap.id, date.date)
#     if not db_entry:
#         raise HTTPException(status_code=400, detail="Not Finished")
#     return entries.remove_today(db, db_entry)
