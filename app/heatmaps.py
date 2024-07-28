from fastapi import HTTPException, status, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import app
from .database import models, schemas
from .functions import users, heatmaps, entries
from .functions.authentication import user_dependency
from .database.database import get_db


router = APIRouter(prefix="/heatmaps", tags=["Heatmaps"])


@router.get("/single/{heatmap}", response_model=schemas.Heatmap)
def get_user_heatmap(
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
    return db_heatmap


@router.get("/all/", response_model=list[schemas.Heatmap])
def get_user_all_heatmaps(user_auth: user_dependency, db: Session = Depends(get_db)):
    user_id = user_auth["id"]
    db_user = users.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return heatmaps.get_user_all_heatmaps(db_user)


@router.get("/streak/{heatmap}/", response_model=list[schemas.HeatmapEntry])
def get_heatmap_streak(
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
    all_entries = entries.get_all_entries(db_heatmap)
    return heatmaps.get_heatmap_streak(all_entries)


@router.post("/create/", response_model=schemas.Heatmap)
def create_heatmap(
    user_auth: user_dependency,
    heatmap: schemas.HeatmapCreate,
    db: Session = Depends(get_db),
):
    user_id = user_auth["id"]
    db_user = users.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_heatmap = heatmaps.get_heatmap_title(db, user_id, heatmap.title)
    if db_heatmap:
        raise HTTPException(status_code=404, detail="Title already taken")

    return heatmaps.create_heatmap(db, user_id, heatmap)


@router.put("/change/{heatmap}/", response_model=schemas.Heatmap)
def change_heatmap(
    user_auth: user_dependency,
    heatmap: str,
    new_heatmap: schemas.HeatmapChange,
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
    return heatmaps.change_heatmap(db, db_heatmap, new_heatmap)


@router.delete("/remove/{heatmap}/", response_model=schemas.Heatmap)
def remove_heatmap(
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
    return heatmaps.remove_heatmap(db, db_heatmap)
