from fastapi import HTTPException, status
from sqlalchemy import null
from routers.schemas import CategoryBase, CategoryDisplay
from sqlalchemy.orm.session import Session
import datetime
from database.models import DbCategory, DbProduct


def create(db: Session, request: CategoryBase):
    new_category = DbCategory(
        name = request.name,
        image_url = request.image_url,
        parent_cat_id = request.parent_cat_id,
        is_activate = request.is_activate,
        admin_id = request.admin_id,
        creation_timestamp = datetime.datetime.now(),
        updated_timestamp = datetime.datetime.now()
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_all(db: Session):
    return db.query(DbCategory).all()

def get_item(id: int, db: Session):
    try:
        category = db.query(DbCategory).filter(DbCategory.id == id).first()
        if category!= null:
            return category
    except:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Category with id {id} was not found.')
    return 'ok'

def update(db:Session, id: int, request: CategoryBase):
    category = db.query(DbCategory).filter(DbCategory.id == id).first()
    #Handle some exceptions
    category.update({
        DbCategory.name : request.name,
        DbCategory.image_url: request.image_url,
    })
    db.commit()
    return 'ok'

def delete(id: int, db: Session):
    try:
        cat = db.query(DbCategory).filter(DbCategory.id == id).first()
        db.delete(cat)
        db.commit()
        return 'ok'
    except:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Category with id {id} was not found.')

