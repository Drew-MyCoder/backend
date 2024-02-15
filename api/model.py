from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from datetime import datetime, UTC
from api.database import Base


class DBUserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String, default='user')
    created_at = Column(DateTime, default=datetime.now(UTC))


class DBPrayertable(Base):
    __tablename__ = "prayers"
    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now(UTC))



class DBTestimonyTable(Base):
    __tablename__ = "testimony"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    # user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now(UTC))