from fastapi import HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy import and_
from routers.schemas import OrderBase, OrderDisplay
from sqlalchemy.orm.session import Session
import datetime
from database.models import DbMessage, DbOrder, DbProduct, DbUser

def create(db: Session, request: OrderBase, buyer_id: int):
    product = db.query(DbProduct).filter(DbProduct.id == request.product_id).first()
    if(request.quantity > product.quantity):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='The ordered quantity is not available right now.')
    calc_total_price = product.price * request.quantity
    product.quantity = product.quantity - request.quantity
    new_product = db.query(DbProduct).filter(DbProduct.id == request.product_id)
    new_product.update(
        {DbOrder.quantity: product.quantity}
    )
    db.commit()
    new_order = DbOrder(
        buyer_id = buyer_id,
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

def get_all(db: Session, user_id: int) -> Page[OrderDisplay]:
    try:
        user = db.query(DbUser).filter(DbUser.id == user_id).first()
        if user.is_admin:
            return paginate(db.query(DbOrder).order_by(DbOrder.creation_timestamp).all())
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f'User with id {user_id} is not an admin, so you can not reach this content.')
    except:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f'User with id {user_id} is not an admin, so you can not reach this content.')


def get_user_orders(id: int, db: Session) -> Page[OrderDisplay]:
    try:
        query= db.query(DbOrder).filter(DbOrder.buyer_id == id).order_by(DbOrder.creation_timestamp).all()
        if query:
            return paginate(query)
        else:
             raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id {id} has no orders yet.')
    except:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id {id} has no orders yet.')

def get_item(id: int, db: Session, user_id: int):
    order = db.query(DbOrder).filter(DbOrder.id == id).first()
    if not order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Order with id {id} was not found.')
    if  order.buyer_id == user_id:
        return order
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'You do not have an access permission to this order with id {id}.')

def delete(id: int, db: Session):
    order = db.query(DbOrder).filter(DbOrder.id == id).first()
    if not order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Order with id {id} was not found.')
    db.delete(order)
    #order.is_activate = False
    db.commit()
    return 'ok'