from pydantic import BaseModel
from datetime import date


class HeatmapEntryBase(BaseModel):
    finished_date: date


class HeatmapEntry(HeatmapEntryBase):
    user_id: int
    heatmap_id: int


class HeatmapBase(BaseModel):
    title: str
    description: str | None = None


class HeatmapCreate(HeatmapBase):
    pass


class Heatmap(HeatmapBase):
    id: int
    user_id: int
    dates: list[HeatmapEntry] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    heatmaps: list[Heatmap] = []

    class Config:
        orm_mode = True
