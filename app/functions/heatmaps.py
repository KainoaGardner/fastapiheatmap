from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..database import models, schemas


def get_all_entries(heatmap: schemas.Heatmap):
    return heatmap.entries


def get_user_heatmap(db: Session, user_id, heatmap_id):
    return (
        db.query(models.Heatmaps)
        .filter(models.Heatmaps.user_id == user_id, models.Heatmaps.id == heatmap_id)
        .first()
    )


def get_heatmap_title(db: Session, user_id: int, heatmap_title: str):
    return (
        db.query(models.Heatmaps)
        .filter(
            models.Heatmaps.user_id == user_id, models.Heatmaps.title == heatmap_title
        )
        .first()
    )


def change_heatmap(
    db: Session, db_heatmap: schemas.Heatmap, new_heatmap: schemas.HeatmapChange
):
    if new_heatmap.title:
        db_heatmap.title = new_heatmap.title
    if new_heatmap.description:
        db_heatmap.description = new_heatmap.description

    db.commit()
    db.refresh(db_heatmap)

    return db_heatmap


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
