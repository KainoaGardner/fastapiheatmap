from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    heatmaps = relationship("Heatmaps", backref="users")


class Heatmaps(Base):
    __tablename__ = "heatmaps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    entries = relationship("HeatmapEntries", backref="heatmaps")


class HeatmapEntries(Base):
    __tablename__ = "heatmapdates"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), default=func.now(), index=True)
    heatmap_id = Column(Integer, ForeignKey("heatmaps.id"))
