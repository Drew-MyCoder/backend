from auth import schema, utils
from fastapi import APIRouter, Depends, HTTPException
from api.db.database import get_db
from auth import model, crud
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
    existing_email = crud.get_user_by_email(
        email=user_info.email, db=db
    )
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user.hashed_password = utils.pwd_context.hash(user_info.password)

    _user = crud.create_user(db_user=db_user, db=db)
    return _user


