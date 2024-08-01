from fastapi import HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy import or_
from routers.schemas import MessageBase, MessageDisplay
from sqlalchemy.orm.session import Session
import datetime
from database.models import DbMessage, DbUser

def create(db: Session, request: MessageBase, user_id: int):
    try:
        receiver = db.query(DbUser).filter(DbUser.id == request.receiver_id).first()
        if not receiver:
            id = request.receiver_id 
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'User with id {id} was not found, so you can not send him/her a message.')
        else:
            new_msg = DbMessage(
                sender_id = user_id,
                receiver_id = request.receiver_id,
                msg_txt = request.msg_txt,
                msg_status = request.msg_status,
                creation_timestamp = datetime.datetime.now(),
                updated_timestamp = datetime.datetime.now(),
                updated_status_timestamp = datetime.datetime.now()
            )
            db.add(new_msg)
            db.commit()
            db.refresh(new_msg)
            return new_msg
    except:
        id = request.receiver_id 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'User with id {id} was not found, so you can not send him/her a message.')

def get_all(user_id: int, db: Session) -> Page[MessageDisplay]:
    try:
        user = db.query(DbUser).filter(DbUser.id == user_id).first()
        if user.is_admin:
            return paginate(db.query(DbMessage).order_by(DbMessage.creation_timestamp).all())
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f'User with id {user_id} is not an admin, so you can not reach this content.')
    except:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f'User with id {user_id} is not an admin, so you can not reach this content.')


def get_user_messages(user_id: int, db: Session) -> Page[MessageDisplay]:
    return paginate(db.query(DbMessage).filter(or_(DbMessage.receiver_id == user_id , DbMessage.sender_id == user_id )).order_by(DbMessage.creation_timestamp).all())

def get_item(id: int, db: Session, user_id: int):
    message = db.query(DbMessage).filter(DbMessage.id == id).first()
    if message:
        if message.sender_id == user_id or message.receiver_id == user_id:
            return message
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f'You do not have an access permission to this message with id {id}.')
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Message with id {id} was not found.')

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
    msg = db.query(DbMessage).filter(DbMessage.id == id).first()
    if msg:
        if msg.sender_id == user_id:
            db.delete(msg)
            db.commit()
            return f'Message with id {id} has been deleted.'
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f'You do not have a permission to delete this message with id {id}.')
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Message with id {id} was not found.')
