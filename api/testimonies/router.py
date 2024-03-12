from api.testimonies import schema, crud
from api.auth import model
from fastapi import APIRouter, Depends
from api.database import get_db
from fastapi import HTTPException
from custom_error import NotFoundError


router = APIRouter(prefix="/testimonies", tags=["Testimony"])


@router.post("/", response_model=schema.Testimony)
async def create_testimony(
    testimony_detail: schema.TestimonyCreate, db=Depends(get_db)
) -> schema.Testimony:
    new_testimony = model.DBTestimonyTable(
        title=testimony_detail.title,
        body=testimony_detail.body,
    )

    _testimony = crud.create_testimony(db_testimony=new_testimony, db=db)
    return _testimony


@router.get("/", response_model=list[schema.Testimony])
async def get_all_testimonies(db=Depends(get_db)):
    return crud.read_testimonies(db)


@router.get("/{id: int}")
async def get_testimonies_by_id(id: int, db=Depends(get_db)):
    return crud.read_testimony_by_id(testimony_id=id, db=db)


@router.delete("/{id: int}")
async def delete_testimony_by_id(id: int, db=Depends(get_db)):
    try:
        testimony = crud.find_testimony_by_id(testimony_id=id, db=db)
        return crud.delete_testimony(testimony=testimony, db=db)
    except NotFoundError:
        raise HTTPException(404, "Testimony with this id does not exist")


@router.patch("/{id: int}", response_model=schema.TestimonyUpdate)
async def patch_testimony_by_id(
    id: int, update_info: schema.TestimonyUpdate, db=Depends(get_db)
):
    try:
        testimony = crud.find_testimony_by_id(id, db)
        if update_info.title:
            testimony.title = update_info.title
        if update_info.body:
            testimony.body = update_info.body
    except NotFoundError:
        raise HTTPException(404, "Testimony with this id cannot be updated")

    return crud.update_testimony(db_testimony=testimony, db=db)
