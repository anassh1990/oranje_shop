import shutil
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from routers.schemas import CategoryBase, CategoryDisplay
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_category
import string
import random

router = APIRouter(
    prefix='/category',
    tags=['category']
)

@router.post('/create', response_model = CategoryDisplay)
def create(request: CategoryBase, db: Session = Depends(get_db)):
    return db_category.create(db, request)

@router.put('/update/{id}', response_model = CategoryDisplay)
def update(request: CategoryBase, db: Session = Depends(get_db)):
    return db_category.update(db, request)

@router.get('/all', response_model= List[CategoryDisplay])
def categories(db: Session = Depends(get_db)):
    return db_category.get_all(db)

@router.get('/item/{id}', response_model= CategoryDisplay)
def get_item(id: int, db: Session = Depends(get_db)):
    return db_category.get_item(id, db)

@router.delete('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    return db_category.delete(id, db)

@router.post('/image')
def upload_image(image: UploadFile = File(...)):
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.',1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}