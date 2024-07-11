from typing import List
from pydantic import BaseModel
from datetime import datetime

#Sub Category inside CategoryDisplay
class Category(BaseModel):
    id: int
    name : str
    image_url : str
    parent_cat_id : int
    admin_id : int
    is_activate : bool
    creation_timestamp: datetime
    class Config():
        orm_mode = True

#Product inside CategoryDisplay
class Product(BaseModel):
    id: int
    name : str
    image_url : str
    price : float
    quantity : int
    status : int
    is_activate : bool
    class Config():
        orm_mode = True

#Product inside ProductDisplay
class User(BaseModel):
    id: int
    fname: str
    lname: str
    email: str
    is_admin: bool
    class Config():
        orm_mode = True

class CategoryBase(BaseModel):
    name : str
    image_url : str
    parent_cat_id : int
    admin_id : int
    is_activate: bool

class CategoryDisplay(BaseModel):
    id: int
    name : str
    image_url : str
    creation_timestamp: datetime
    parent_cat_id: int
    is_activate: bool
    sub_cat_items: List[Category] = []
    prod_items: List [Product] = []
    admin_id : int
    class Config():
        orm_mode = True

class ProductBase(BaseModel):
    name : str
    image_url : str
    description : str
    price : float
    quantity : int
    status : int
    is_activate : bool
    cat_id : int
    seller_id : int

class ProductDisplay(BaseModel):
    id: int
    name : str
    image_url : str
    description : str
    price : float
    quantity : int
    status : int
    is_activate : bool
    category_of_product : Category
    seller_of_product : User
    creation_timestamp: datetime
    updated_status_timestamp: datetime
    class Config():
        orm_mode = True

class UserBase(BaseModel):
    fname: str
    lname: str
    email: str
    password: str
    is_admin: bool= False

class UserDisplay(BaseModel):
    id: int
    fname: str
    lname: str
    email: str
    password: str
    is_admin: bool
    creation_timestamp: datetime
    prod_items: List [Product] = []
    class Config():
        orm_mode = True

class UserAuth(BaseModel):
    id: int
    email: str