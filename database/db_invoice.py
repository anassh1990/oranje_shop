from fastapi import HTTPException, status
from fastapi_pagination import Page, paginate
from routers.schemas import InvoiceBase, InvoiceDisplay
from sqlalchemy.orm.session import Session
import datetime
from database.models import DbInvoice, DbOrder, DbUser

def create(db: Session, request: InvoiceBase):
    new_invoice = DbInvoice(
        payment_mehtod = request.payment_mehtod, #0: Paybal, 1: DebitCard, 2: CreditCard..
        total_price = request.total_price,
        barcode_url = request.barcode_url,
        creation_timestamp = datetime.datetime.now(),
        updated_timestamp = datetime.datetime.now()
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice

def get_user_invoices(db: Session, user_id:int) -> Page[InvoiceDisplay]:
    query = db.query(DbInvoice).join(DbOrder).filter(DbInvoice.id == DbOrder.invoice_id).filter(DbOrder.buyer_id == user_id).order_by(DbInvoice.creation_timestamp).all()
    return paginate(query)

def get_all(db: Session, user_id: int) -> Page[InvoiceDisplay]:
    try:
        user = db.query(DbUser).filter(DbUser.id == user_id).first()
        if user.is_admin:
            return paginate(db.query(DbInvoice).order_by(DbInvoice.creation_timestamp).all())
        else:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f'User with id {user_id} is not an admin, so you can not reach this content.')
    except:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f'User with id {user_id} is not an admin, so you can not reach this content.')

def get_item(id: int, db: Session, user_id: int):
    invoice = db.query(DbInvoice).filter(DbInvoice.id == id).first()
    if invoice:
        invoice = db.query(DbInvoice).join(DbOrder).filter(DbInvoice.id == DbOrder.invoice_id).filter(DbOrder.buyer_id == user_id).where(DbInvoice.id == id).order_by(DbInvoice.creation_timestamp).first()
        if invoice:
            return invoice
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f'User has no access permission to this invoice with id {id}.')
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Invoice with id {id} was not found.')

# def update(db:Session, id: int, request: CategoryBase):
#     category = db.query(DbMessage).filter(DbMessage.id == id).first()
#     #Handle some exceptions
#     category.update({
#         DbMessage.name : request.name,
#         DbMessage.image_url: request.image_url,
#     })
#     db.commit()
#     return 'ok'

def delete(id: int, db: Session, user_id: int):
    invoice = db.query(DbInvoice).filter(DbInvoice.id == id).first()
    if invoice:
        invoice = db.query(DbInvoice).join(DbOrder).filter(DbInvoice.id == DbOrder.invoice_id).filter(DbOrder.buyer_id == user_id).first()
        if invoice:
            db.delete(invoice)
            db.commit()
            return f'Invoice with id {id} has been deleted.'
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f'User has no permission to delete this invoice with id {id}.')
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Invoice with id {id} was not found.')
