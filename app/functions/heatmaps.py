from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..database import models, schemas


def get_user_heatmaps(db: Session, user_id: int):
    return db.query(models.Heatmaps).filter(models.Heatmaps.user_id == user_id).all()


def get_heatmap_title(db: Session, user_id: int, heatmap_title: str):
    return (
        db.query(models.Heatmaps)
        .filter(
            models.Heatmaps.user_id == user_id, models.Heatmaps.title == heatmap_title
        )
        .first()
    )


def create_heatmap(db: Session, user_id: int, heatmap: schemas.HeatmapCreate):
    db_heatmap = models.Heatmaps(
        title=heatmap.title, description=heatmap.description, user_id=user_id
    )
    db.add(db_heatmap)
    db.commit()
    db.refresh(db_heatmap)
    return db_heatmap


def remove_heatmap(db: Session, user_id: int, heatmap_id: int):
    heatmap = (
        db.query(models.Heatmaps)
        .filter(models.Heatmaps.id == heatmap_id, models.Heatmaps.user_id == user_id)
        .first()
    )
    db.delete(heatmap)
    db.commit()
    return heatmap
