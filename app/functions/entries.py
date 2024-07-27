from fastapi import APIRouter
from sqlalchemy.orm import Session
from datetime import date

from ..database import models, schemas


def get_all_entries(heatmap: schemas.Heatmap) -> list:
    return heatmap.entries


def check_today(
    db: Session, user_id: int, heatmap_id: int, date: date
) -> schemas.HeatmapEntry:
    return (
        db.query(models.HeatmapEntries)
        .filter(
            models.HeatmapEntries.heatmap_id == heatmap_id,
            models.HeatmapEntries.date == date,
        )
        .first()
    )


def remove_today(db: Session, db_entry) -> schemas.HeatmapEntry:
    db.delete(db_entry)
    db.commit()
    return db_entry


def create_entry(db: Session, heatmap_id: int, date: date) -> schemas.HeatmapEntry:
    db_entry = models.HeatmapEntries(date=date, heatmap_id=heatmap_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
