from typing import List
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from auth.oauth2 import get_current_user
from database.database import get_db
from routers.schemas import  OrderBase, OrderDisplay, UserAuth
from sqlalchemy.orm import Session
from database import db_order

router = APIRouter(
    prefix='/order',
    tags=['order']
)

@router.post('', response_model = OrderDisplay)
def create_order(request: OrderBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_order.create(db, request, current_user.id)

@router.get('/admin/',response_model= Page[OrderDisplay])
async def get_orders_list(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)) -> Page[OrderDisplay]:
    return db_order.get_all(db, current_user.id)

@router.get('/',response_model= Page[OrderDisplay])
async def get_user_orders(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)) -> Page[OrderDisplay]:
    return db_order.get_user_orders(current_user.id, db)

@router.get('/{id}', response_model= OrderDisplay)
def get_order(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_order.get_item(id, db, current_user.id)

@router.delete('/{id}')
def delete_order(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_order.delete(id, db)
