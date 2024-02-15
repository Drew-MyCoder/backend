from pydantic import BaseModel


class UserBase(BaseModel):
    firstname: str
    lastname: str 
    email: str


class UserCreate(UserBase):
    role: str = 'user'

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None


class UserOutput(UserBase):
    id: int
    username: str
    role: str 


class User(UserOutput):
    hashed_password: str
    