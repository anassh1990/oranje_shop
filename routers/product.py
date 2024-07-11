import shutil
from fastapi import APIRouter, Depends, File, UploadFile
from routers.schemas import ProductBase, ProductDisplay, UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_product
from typing import List
import string
import random
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/product',
    tags=['product']
)

@router.post('/create')
def create(request: ProductBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_product.create(db, request)

@router.get('/all',response_model= List[ProductDisplay])
def categories(db: Session = Depends(get_db)):
    return db_product.get_all(db)

@router.delete('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    return db_product.delete(id, db)

@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.',1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}