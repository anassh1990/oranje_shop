from typing import List
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from auth.oauth2 import get_current_user
from routers.schemas import InvoiceBase, InvoiceDisplay, UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_invoice

router = APIRouter(
    prefix='/invoice',
    tags=['invoice']
)

@router.post('/', response_model = InvoiceDisplay)
def create_invoice(request: InvoiceBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_invoice.create(db, request)

# @router.put('/{id}', response_model = MessageDisplay)
# def update(request: MessageBase, db: Session = Depends(get_db)):
#     return db_category.update(db, request)

@router.get('/admin/', response_model= Page[InvoiceDisplay])
async def get_invoices_list(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user))-> Page[InvoiceDisplay]:
    return db_invoice.get_all(db, current_user.id)

@router.get('/', response_model= Page[InvoiceDisplay])
async def get_user_invoices(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user))-> Page[InvoiceDisplay]:
    return db_invoice.get_user_invoices(db, current_user.id)

@router.get('/{id}', response_model= InvoiceDisplay)
def get_invoice(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_invoice.get_item(id, db, current_user.id)

@router.delete('/{id}')
def delete_invoice(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_invoice.delete(id, db, current_user.id)