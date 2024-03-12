from pydantic import BaseModel


class TestimonyBase(BaseModel):
    title: str
    body: str


class TestimonyCreate(TestimonyBase):
    pass


class TestimonyUpdate(BaseModel):
    title: str | None = None
    body: str | None = None


class Testimony(TestimonyBase):
    id: int

