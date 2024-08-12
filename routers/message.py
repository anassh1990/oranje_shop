from typing import List
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from auth.oauth2 import get_current_user
from routers.schemas import MessageBase, MessageDisplay, UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_message

router = APIRouter(
    prefix='/message',
    tags=['message']
)

@router.post('/', response_model = MessageDisplay)
def create_message(request: MessageBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_message.create(db, request, current_user.id)

# @router.put('/{id}', response_model = MessageDisplay)
# def update(request: MessageBase, db: Session = Depends(get_db)):
#     return db_category.update(db, request)

@router.get('/admin/', response_model= Page[MessageDisplay])
async def get_messages_list(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)) -> Page[MessageDisplay]:
    return db_message.get_all(current_user.id, db)

@router.get('/', response_model= Page[MessageDisplay])
async def get_user_messages(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)) -> Page[MessageDisplay]:
    return db_message.get_user_messages(current_user.id, db)

@router.get('/{id}', response_model= MessageDisplay)
def get_message(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_message.get_item(id, db, current_user.id)

@router.delete('/{id}')
def delete_message(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_message.delete(id, db, current_user.id)