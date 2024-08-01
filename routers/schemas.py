from typing import List, Optional
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
    class Config():
        from_attributes = True

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
        from_attributes = True

#User inside ProductDisplay(seller), CategoryDisplay(owner_admin)
class User(BaseModel):
    id: int
    fname: str
    lname: str
    email: str
    is_admin: bool
    class Config():
        from_attributes = True

#Schema of creating Category or SubCategory
class CategoryBase(BaseModel):
    name : str
    image_url : str
    parent_cat_id : int
    admin_id : int
    is_activate: bool = True

class CategoryDisplay(BaseModel):
    id: int
    name : str
    image_url : str
    creation_timestamp: datetime
    updated_timestamp: datetime
    parent_cat_id: int
    is_activate: bool
    sub_cat_items: List[Category] = []
    prod_items: List [Product] = []
    owner_admin : Optional[User] = None
    class Config():
        from_attributes = True

#Schema of creating Product
class ProductBase(BaseModel):
    name : str
    image_url : str
    description : str
    price : float
    quantity : int
    status : int
    is_activate : bool = True
    cat_id : int
    seller_id : int #Owner of the product
    location: str # to include location information

class ProductDisplay(BaseModel):
    id: int
    name : str
    image_url : str
    description : str
    price : float
    quantity : int
    status : int
    is_activate : bool 
    category_of_product : Optional[Category] = None
    seller_of_product : Optional[User] = None
    location: Optional[str] = 'Unknown' # to show location information
    creation_timestamp: datetime
    updated_status_timestamp: datetime
    class Config():
        from_attributes = True

#Schema of creating User
class UserBase(BaseModel):
    fname: str
    lname: str
    email: str
    password: str
    is_admin: bool = False
    is_activate: bool = True

class UserDisplay(BaseModel):
    id: int
    fname: str
    lname: str
    email: str
    password: str
    is_admin: bool
    is_activate: bool
    creation_timestamp: datetime
    updated_timestamp: datetime
    prod_items: List [Product] = []
    class Config():
        from_attributes = True

#Schema of creating Order
class OrderBase(BaseModel):
    #buyer_id: int
    product_id: int
    status: int
    quantity: int
    invoice_id: int
    is_activate: bool = True

#Order inside User, Invoice (User Orders- Invoice Orders)
#class Order(BaseModel):
#    id: int
#    ordered_product: Product


class Invoice(BaseModel):
    id: int
    creation_timestamp: datetime
    updated_timestamp: datetime
    payment_mehtod: int #0: Paybal, 1: DebitCard, 2: CreditCard..
    total_price: float
    barcode_url: str

class OrderDisplay(BaseModel):
    id: int
    status: int
    quantity: int
    total_price: float
    creation_timestamp: datetime
    updated_timestamp: datetime
    updated_status_timestamp: datetime
    buyer_of_product: User
    ordered_product: Product
    related_invoice: Invoice
    is_activate: bool
    class Config():
        from_attributes = True

class InvoiceBase(BaseModel):
    payment_mehtod: int #0: Paybal, 1: DebitCard, 2: CreditCard..
    total_price: float
    barcode_url: str

class InvoiceDisplay(BaseModel):
    id: int
    creation_timestamp: datetime
    updated_timestamp: datetime
    payment_mehtod: int #0: Paybal, 1: DebitCard, 2: CreditCard..
    total_price: float
    barcode_url: str
    products_per_invoice: List[OrderDisplay]
    class Config():
        from_attributes = True
 
class UserAuth(BaseModel):
    id: int
    email: str

class MessageBase(BaseModel):
    #sender_id: int
    receiver_id: int
    msg_txt: str
    msg_status: int

class MessageDisplay(BaseModel):
    id: int
    sender: User
    receiver: User
    msg_txt: str
    msg_status: int
    creation_timestamp: datetime
    updated_timestamp: datetime
    updated_status_timestamp: datetime