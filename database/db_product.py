from fastapi import HTTPException, status
from routers.schemas import ProductBase
from sqlalchemy.orm.session import Session
import datetime
from database.models import DbProduct

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

def get_all(db: Session):
    return db.query(DbProduct).all()

def delete(id: int, db: Session):
    product = db.query(DbProduct).filter(DbProduct.id == id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Product with id {id} was not found.')
    #db.delete(product)
    product.is_activate = False
    db.commit()
    return 'ok'