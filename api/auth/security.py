import os

# from enum import Enum
from datetime import datetime, timedelta, UTC

# from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from dotenv import load_dotenv
from api.database import get_db
from api.auth import crud, schema, model

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class NoMatchError(Exception):
    pass


# Util functions


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user_with_email(email: str, password: str, db):
    user = crud.find_user_by_email(email=email, db=db)

    if not verify_password(password, user.hashed_password):
        raise NoMatchError()

    return user


# def authenticate_user(email_or_phone_number: str, password: str, db):
#     # user = crud.find_user_by_username(username=username,db=db)
#     user = crud.get_user_by_phone_number(phone_number=email_or_phone_number, db=db)
#     if user is None:
#         user = crud.get_user_by_email(email=email_or_phone_number, db=db)

#     if user is None:
#         raise NoMatchError()

#     if not verify_password(password, user.hashed_password):
#         raise NoMatchError()

#     return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=15)

    expire: datetime = datetime.now(UTC) + expires_delta

    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def validate_access_token(token: str = Depends(oauth2_scheme)):
    pass  # TODO


async def validate_refresh_token(db, refresh_token) -> str:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        expire = payload.get("exp")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = (
            db.query(model.DBRefreshTokenTable)
            .filter(model.DBRefreshTokenTable.token == refresh_token)
            .first()
        )

        if token_data is None or (expire and expire < datetime.now(UTC)):
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # db.delete(token_data)
        # db.commit()
        return username
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Refresh token expired.")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# CRUD
async def get_current_user(
    token: str = Depends(oauth2_scheme), db=Depends(get_db)
) -> model.DBUserTable:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="access token expired")
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(username=token_data.username, db=db)

    if user is None:
        raise credentials_exception

    return user


# def has_permission(permission: str):
#     def decorator(func):
#         async def wrapper(
#             current_user: model.DBUserTable = Depends(get_current_user), *args, **kwargs
#         ):
#             if permission in current_user.roles:
#                 return await func(current_user, *args, **kwargs)
#             else:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
#                 )

#         return wrapper

#     return decorator


# def abfuscate_email(email, replacement_char="***"):
#     parts = email.split("@")
#     return f"{parts[0][:4]}{replacement_char}{parts[-1]}"
