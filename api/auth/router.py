from api.auth import schema, crud, model
from api.auth import utils
from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from api.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(prefix = '/auth', tags= ['Auth'])


@router.post("/signup", response_model=schema.User)
async def register_user(
    user_info: schema.UserCreate, db=Depends(get_db)
) -> schema.User:
    db_user = model.DBUserTable(
        email=user_info.email,
        firstname=user_info.firstname,
        lastname=user_info.lastname,
    )
    existing_email = crud.read_user_by_email(
        email=user_info.email, db=db
    )
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user.hashed_password = utils.pwd_context.hash(user_info.password)

    _user = crud.create_user(db_user=db_user, db=db)
    return _user


@router.post("/login")
async def login_via_email(
    login_details: schema.UserLogin, db=Depends(get_db)
):
    try:
        user = crud.find_user_by_email(username=login_details.email, db=db)

        access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = utils.create_access_token(
            data={"sub": user.username, "roles": user.roles},
            expires_delta=access_token_expires,
        )
        new_refresh_token = utils.create_refresh_token({"sub": user.username})

        response_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.username,
            "roles": user.roles,
        }
        response = JSONResponse(content=response_data)

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            # secure=True, # Only send over HTTPS
            # expires=timedelta(days=7), # Adjust expiration as needed
            # samesite="lax",  # Mitiagte CSRF
        )

        return response
    except crud.NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail="User to be verified is incorrect",
        ) from e


@router.post("/refresh")
async def refresh_access_token_endpoint(
    refresh_token=Depends(oauth2_scheme), db=Depends(get_db)
):
    username = utils.validate_refresh_token(db=db, refresh_token=refresh_token)

    user = crud.get_user_by_username(username=str(username), db=db)

    access_token = utils.create_access_token({"sub": username, "roles": user.roles})
    new_refresh_token = utils.create_refresh_token({"sub": username})
    response = Response(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.username,
            "roles": user.roles,
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        # secure=True, # Only send over HTTPS
        # expires=timedelta(days=7), # Adjust expiration as needed
        # samesite="lax",  # Mitiagte CSRF
    )
    return response