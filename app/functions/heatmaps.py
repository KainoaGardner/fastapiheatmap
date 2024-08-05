from sqlalchemy.orm import Session

from ..database import models, schemas
from datetime import date, timedelta


def get_user_all_heatmaps(user: schemas.User) -> list:
    return user.heatmaps


def get_user_heatmap(db: Session, user_id, heatmap_id) -> schemas.Heatmap:
    return (
        db.query(models.Heatmaps)
        .filter(models.Heatmaps.user_id == user_id, models.Heatmaps.id == heatmap_id)
        .first()
    )


def get_heatmap_title(db: Session, user_id: int, heatmap_title: str) -> schemas.Heatmap:
    return (
        db.query(models.Heatmaps)
        .filter(
            models.Heatmaps.user_id == user_id, models.Heatmaps.title == heatmap_title
        )
        .first()
    )


def get_heatmap_streak(entries: list[schemas.HeatmapEntry]):
    entry_dates = {}
    for entry in entries:
        entry_dates.update({entry.date: entry})

    streak = []
    check_day = date.today()
    while check_day in entry_dates:
        streak.append(entry_dates[check_day])
        check_day = check_day - timedelta(days=1)

    return streak


def change_heatmap(
    db: Session, db_heatmap: schemas.Heatmap, new_heatmap: schemas.HeatmapChange
) -> schemas.Heatmap:
    if new_heatmap.title:
        db_heatmap.title = new_heatmap.title
    if new_heatmap.description:
        db_heatmap.description = new_heatmap.description

    db.commit()
    db.refresh(db_heatmap)

    return db_heatmap


def create_heatmap(
    db: Session, user_id: int, heatmap: schemas.HeatmapCreate
) -> schemas.Heatmap:
    db_heatmap = models.Heatmaps(
        title=heatmap.title, description=heatmap.description, user_id=user_id
    )
    db.add(db_heatmap)
    db.commit()
    db.refresh(db_heatmap)
    return db_heatmap


def remove_heatmap(db, heatmap) -> schemas.Heatmap:
    db.delete(heatmap)
    db.commit()
    return heatmap
