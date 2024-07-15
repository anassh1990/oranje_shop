from fastapi import HTTPException, status
from routers.schemas import OrderBase
from sqlalchemy.orm.session import Session
import datetime
from database.models import DbOrder, DbProduct

def create(db: Session, request: OrderBase):
    product = db.query(DbProduct).filter(DbProduct.id == request.product_id).first()
    if(request.quantity > product.quantity):
        return HTTPException(status_code=402, detail='The ordered quantity is not available right now.')
    calc_total_price = product.price * request.quantity
    new_order = DbOrder(
        buyer_id = request.buyer_id,
        product_id = request.product_id,
        status = request.status,
        quantity = request.quantity,
        total_price = calc_total_price,
        invoice_id = request.invoice_id,
        is_activate = request.is_activate,
        creation_timestamp = datetime.datetime.now(),
        updated_timestamp = datetime.datetime.now(),
        updated_status_timestamp = datetime.datetime.now()
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def get_all(db: Session):
    return db.query(DbOrder).all()

def delete(id: int, db: Session):
    order = db.query(DbOrder).filter(DbOrder.id == id).first()
    if not order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Order with id {id} was not found.')
    db.delete(order)
    #order.is_activate = False
    db.commit()
    return 'ok'