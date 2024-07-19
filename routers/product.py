import shutil
from fastapi import APIRouter, Depends, File, UploadFile
from routers.schemas import ProductBase, ProductDisplay, UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_product
from typing import List, Optional
import string
import random
from auth.oauth2 import get_current_user
from database import models

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

@router.get("/search", response_model=List[ProductDisplay])
def search_products(category: Optional[str] = None, keyword: Optional[str] = None, location: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.DbProduct)
    
    if category:
        query = query.join(models.DbCategory).filter(models.DbCategory.name == category)
    if keyword:
        query = query.filter(models.DbProduct.name.contains(keyword) | models.DbProduct.description.contains(keyword))
    if location:
        query = query.filter(models.DbProduct.location == location)
    
    products = query.all()
    return products