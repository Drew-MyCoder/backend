from api import model 



def read_prayers(db):
    return db.query(model.DBPrayerTable).all()


def read_prayer_by_id(prayer_id, db):
    return db.query(model.DBPrayerTable).filter(model.DBPrayerTable.id==prayer_id).first()


def create_prayer(db_prayer: model.DBPrayerTable, db):
    db.add(db_prayer)
    db.commit()
    db.refresh(db_prayer)
    return db_prayer


def update_prayer(db_prayer: model.DBPrayerTable, db):
    db.commit()
    db.refresh(db_prayer)
    return db_prayer


def delete_prayer(prayer_id: int, db):
    prayer = db.query(model.DBPrayerTable).filter(model.DBPrayerTable.id == prayer_id).first()
    db.delete(prayer)
    db.commit()
    return {"message":f"prayer: {prayer_id} has been successfully deleted"}