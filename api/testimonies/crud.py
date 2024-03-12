from api.auth import model
from sqlalchemy.orm import Session
from custom_error import NotFoundError


def read_testimonies(db):
    return db.query(model.DBTestimonyTable).all()


def read_testimony_by_id(testimony_id, db):
    return (
        db.query(model.DBTestimonyTable)
        .filter(model.DBTestimonyTable.id == testimony_id)
        .first()
    )


def find_testimony_by_id(testimony_id, db):
    if (
        db.query(model.DBTestimonyTable)
        .filter(model.DBTestimonyTable.id == testimony_id)
        .first()
        is None
    ):
        raise NotFoundError("Testimony not found")

    return (
        db.query(model.DBTestimonyTable)
        .filter(model.DBTestimonyTable.id == testimony_id)
        .first()
    )


def create_testimony(db_testimony: model.DBTestimonyTable, db):
    db.add(db_testimony)
    db.commit()
    db.refresh(db_testimony)
    return db_testimony


def update_testimony(db_testimony: model.DBTestimonyTable, db: Session):
    db.commit()
    db.refresh(db_testimony)
    return db_testimony


def delete_testimony(testimony: model.DBTestimonyTable, db: Session):
    db.delete(testimony)
    db.commit()

    return {"message": "testimony has been successfully deleted"}
