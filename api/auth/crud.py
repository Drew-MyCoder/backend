from api.auth import model 


class NotFoundError(Exception):
    pass


def read_users(db):
    return db.query(model.DBUserTable).all()


def read_user_by_email(email, db):
    return db.query(model.DBUserTable).filter(model.DBUserTable.email==email).first()


def find_user_by_email(email: str, db) -> model.DBUserTable:
    user = db.query(model.DBUserTable).filter(model.DBUserTable.email==email).first()
    if user is None:
        raise NotFoundError("User not found")

    return db.query(model.DBUserTable).filter(model.DBUserTable.email==email).first()


def read_user_by_id(user_id, db):
    return db.query(model.DBUserTable).filter(model.DBUserTable.id==user_id).first()


def create_user(db_user: model.DBUserTable, db):
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db_user: model.DBUserTable, db):
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(user_id: int, db):
    user = db.query(model.DBUserTable).filter(model.DBUserTable.id == user_id).first()
    db.delete(user)
    db.commit()
    return {"message":f"user: {user_id} has been successfully deleted"}


