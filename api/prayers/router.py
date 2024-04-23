from api.prayers import schema, crud
from api.auth import model
from api.database import get_db
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from custom_error import NotFoundError

router = APIRouter(prefix="/prayers", tags=["Prayers"])


@router.post("/new", response_model=schema.Prayer)
async def create_prayer(
    prayer_detail: schema.PrayerCreate, db=Depends(get_db)
) -> schema.Prayer:
    new_prayer = model.DBPrayertable(
        title=prayer_detail.title,
        description=prayer_detail.description,
    )

    _prayer = crud.create_prayer(db_prayer=new_prayer, db=db)
    return _prayer


@router.get("/all", response_model=list[schema.Prayer])
async def get_all_prayers(db=Depends(get_db)):
    return crud.read_prayers(db)


@router.get("/{id: int}")
async def get_prayers_by_id(id: int, db=Depends(get_db)):
    return crud.read_prayer_by_id(prayer_id=id, db=db)


@router.delete("/{id: int}")
async def delete_prayer_by_id(id: int, db=Depends(get_db)):
    try:
        prayer = crud.find_prayer_by_id(prayer_id=id, db=db)
        return crud.delete_prayer(prayer=prayer, db=db)
    except NotFoundError:
        raise HTTPException(404, "Prayer with this id does not exist")


@router.patch("/{id: int}", response_model=schema.PrayerUpdate)
async def patch_prayer_by_id(
    id: int, update_info: schema.PrayerUpdate, db=Depends(get_db)
):
    try:
        prayer = crud.find_prayer_by_id(id, db)
        if update_info.title:
            prayer.title = update_info.title
        if update_info.description:
            prayer.description = update_info.description
    except NotFoundError:
        raise HTTPException(404, "Prayer with this id cannot be updated")

    return crud.update_prayer(db_prayer=prayer, db=db)
