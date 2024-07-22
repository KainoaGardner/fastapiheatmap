from pydantic import BaseModel
from sqlalchemy import Date
from datetime import date


class HeatmapEntryBase(BaseModel):
    date: date


class HeatmapEntryDate(HeatmapEntryBase):
    pass


class HeatmapEntryCreate(HeatmapEntryBase):
    pass


class HeatmapEntry(HeatmapEntryBase):
    heatmap_id: int


class HeatmapBase(BaseModel):
    title: str
    description: str | None = None


class HeatmapCreate(HeatmapBase):
    pass


class HeatmapChange(BaseModel):
    title: str | None = None
    description: str | None = None


class Heatmap(HeatmapBase):
    id: int
    user_id: int
    entries: list[HeatmapEntry] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserPassword(UserBase):
    password: str


class User(UserBase):
    id: int
    heatmaps: list[Heatmap] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
