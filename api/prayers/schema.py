from pydantic import BaseModel


class PrayerBase(BaseModel):
    title: str
    description: str


class PrayerCreate(PrayerBase):
    pass


class PrayerUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class Prayer(PrayerBase):
    id: int