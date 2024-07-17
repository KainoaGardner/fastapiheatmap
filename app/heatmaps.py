from fastapi import HTTPException, status, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import app
from .database import models, schemas
from .functions import users, heatmaps
from .database.database import get_db


router = APIRouter(prefix="/heatmaps", tags=["Heatmaps"])


@router.get("/{user_id}/heatmaps", response_model=list[schemas.Heatmap])
def get_user_heatmaps(user_id: int, db: Session = Depends(get_db)):
    db_user = users.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return heatmaps.get_user_heatmaps(db, user_id)


@router.post("/{user_id}/create/heatmap", response_model=schemas.Heatmap)
def create_heatmap(
    user_id, heatmap: schemas.HeatmapCreate, db: Session = Depends(get_db)
):
    db_user = users.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_heatmap = heatmaps.get_heatmap_title(db, user_id, heatmap.title)
    if db_heatmap:
        raise HTTPException(status_code=404, detail="Title already taken")

    return heatmaps.create_heatmap(db, user_id, heatmap)


@router.delete("/{user_id}/remove/{heatmap_id}", response_model=schemas.Heatmap)
def remove_heatmap(user_id: int, heatmap_id: int, db: Session = Depends(get_db)):

    return heatmaps.remove_heatmap(db, user_id, heatmap_id)
