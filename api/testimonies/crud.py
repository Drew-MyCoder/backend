from api import model 



def read_testimonies(db):
    return db.query(model.DBTestimonyTable).all()


def read_testimony_by_id(testimony_id, db):
    return db.query(model.DBTestimonyTable).filter(model.DBTestimonyTable.id==testimony_id).first()


def create_testimony(db_testimony: model.DBTestimonyTable, db):
    db.add(db_testimony)
    db.commit()
    db.refresh(db_testimony)
    return db_testimony


def update_testimony(db_testimony: model.DBTestimonyTable, db):
    db.commit()
    db.refresh(db_testimony)
    return db_testimony


def delete_testimony(testimony_id: int, db):
    testimony = db.query(model.DBTestimonyTable).filter(model.DBTestimonyTable.id == testimony_id).first()
    db.delete(testimony)
    db.commit()
    return {"message":f"testimony: {testimony_id} has been successfully deleted"}