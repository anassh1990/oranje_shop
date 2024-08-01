from fastapi import HTTPException, status
from sqlalchemy import null
from routers.schemas import ProductBase, ProductDisplay, UserBase
from sqlalchemy.orm.session import Session
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate
import datetime
from database.models import DbProduct


def log(tag = '', message = ''):
    with open('log.txt', 'a+') as log:
        log.write(f"{tag}: {message}\n")

def create(db: Session, request: ProductBase):
    new_product = DbProduct(
        name = request.name,
        image_url = request.image_url,
        description = request.description,
        price = request.price,
        quantity = request.quantity,
        status = request.status,
        is_activate = request.is_activate,
        cat_id = request.cat_id,
        seller_id = request.seller_id,
        location = request.location or 'Unknown',
        updated_status_timestamp = datetime.datetime.now(),
        creation_timestamp = datetime.datetime.now()
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_all(db: Session) -> Page[ProductDisplay]:
    #return paginate(db.query(DbProduct).order_by(DbProduct.creation_timestamp).all())
    return paginate(db, select(DbProduct).order_by(DbProduct.creation_timestamp))

def get_item(id: int, db: Session):
    try:
        product = db.query(DbProduct).filter(DbProduct.id == id).first()
        if product:
            return product
        else:
             raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} was not found.')
    except:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} was not found.')

def delete(id: int, db: Session):
    product = db.query(DbProduct).filter(DbProduct.id == id).first()
    if not product:
        log(f"{id}", f"HTTP_404_NOT_FOUND - Product with id {id} was not found.")
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Product with id {id} was not found.')
    #db.delete(product)
    product.is_activate = False
    db.commit()
    return 'ok'