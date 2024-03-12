from api.auth import model
from sqlalchemy.orm import Session
from custom_error import NotFoundError


def read_prayers(db):
    return db.query(model.DBPrayertable).all()


def read_prayer_by_id(prayer_id, db):
    return (
        db.query(model.DBPrayertable)
        .filter(model.DBPrayertable.id == prayer_id)
        .first()
    )


def find_prayer_by_id(prayer_id, db):
    if (
        db.query(model.DBPrayertable)
        .filter(model.DBPrayertable.id == prayer_id)
        .first()
        is None
    ):
        raise NotFoundError("Prayer not found")

    return (
        db.query(model.DBPrayertable)
        .filter(model.DBPrayertable.id == prayer_id)
        .first()
    )


def create_prayer(db_prayer: model.DBPrayertable, db):
    db.add(db_prayer)
    db.commit()
    db.refresh(db_prayer)
    return db_prayer


def update_prayer(db_prayer: model.DBPrayertable, db: Session):
    db.commit()
    db.refresh(db_prayer)
    return db_prayer


def delete_prayer(prayer: model.DBPrayertable, db: Session):
    db.delete(prayer)
    db.commit()
    return {"message": "prayer has been successfully deleted"}
