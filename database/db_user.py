from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from database.models import DbUser
from database.hashing import Hash
from fastapi import HTTPException, status
import datetime


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        fname = request.fname,
        lname = request.lname,
        email = request.email,
        password = Hash.bcrypt(request.password), # we need to encyrpt the password
        is_admin = request.is_admin,
        creation_timestamp = datetime.datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(DbUser).all()

def get_user(db:Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'User with id {id} not found')
    return user

def get_user_by_username(db:Session, username: str):
    user = db.query(DbUser).filter(DbUser.email == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'User with username {username} not found')
    return user 

def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'User with id {id} not found')
    user.update({
        DbUser.fname: request.fname,
        DbUser.lname: request.lname,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return 'User data updated!'

def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'User with id {id} not found')
    db.delete(user)
    db.commit()
    return 'User deleted!'