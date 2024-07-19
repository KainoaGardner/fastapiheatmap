from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import Date

from ..database import models, schemas


def check_today(db: Session, heatmap_id: int, date: Date):
    return (
        db.query(models.HeatmapEntries)
        .filter(
            models.HeatmapEntries.heatmap_id == heatmap_id,
            models.HeatmapEntries.date == date,
        )
        .first()
    )


def create_entry(db: Session, heatmap_id: int, new_entry: schemas.HeatmapEntryCreate):
    db_entry = models.HeatmapEntries(date=new_entry.date, heatmap_id=heatmap_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
