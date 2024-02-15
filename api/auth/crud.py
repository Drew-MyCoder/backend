from api import model 



def read_users(db):
    return db.query(model.DBUserTable).all()


def read_user_by_username(username, db):
    return db.query(model.DBUserTable).filter(model.DBUserTable.username==username).first()


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