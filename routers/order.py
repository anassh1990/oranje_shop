from typing import List
from fastapi import APIRouter, Depends
from database.database import get_db
from routers.schemas import OrderBase, OrderDisplay
from sqlalchemy.orm import Session
from database import db_order

router = APIRouter(
    prefix='/order',
    tags=['order']
)

@router.post('')
def create(request: OrderBase, db: Session = Depends(get_db)):
    return db_order.create(db, request)

@router.get('/',response_model= List[OrderDisplay])
def orders(db: Session = Depends(get_db)):
    return db_order.get_all(db)

@router.delete('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    return db_order.delete(id, db)
