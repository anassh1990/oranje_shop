from .database import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm.relationships import Relationship

class DbCategory(Base):
    __tablename__= "category"
    id = mapped_column(Integer, primary_key=True, index=True) #PK
    name = mapped_column(String)
    image_url = mapped_column(String)
    creation_timestamp = mapped_column(DateTime)
    updated_timestamp = mapped_column(DateTime)
    parent_cat_id = mapped_column(Integer, ForeignKey('category.id')) #FK
    sub_cat_items = Relationship("DbCategory")
    prod_items = Relationship('DbProduct', back_populates='category_of_product')
    is_activate = mapped_column(Boolean) #True: activate to show, False: not activate to show
    admin_id = mapped_column(Integer, ForeignKey('user.id')) #FK
    owner_admin = Relationship('DbUser', back_populates='created_catgories')
    

class DbProduct(Base):
    __tablename__= "product"
    id = Column(Integer, primary_key=True, index=True) #PK
    name = Column(String)
    image_url = Column(String)
    description = Column(Integer)
    rate = Column(Float)
    price = Column(Float)
    quantity = Column(Integer)
    location = Column(String)
    status = Column(Integer) # 0:initiated, 1:approved by admin, 2:rejected by admin, 3:soldout
    is_activate = Column(Boolean) #True: activate to show, False: not activate to show
    creation_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime)
    updated_status_timestamp = Column(DateTime)
    cat_id = Column(Integer, ForeignKey('category.id')) #FK
    category_of_product = Relationship('DbCategory', back_populates='prod_items')
    seller_id = Column(Integer, ForeignKey('user.id')) #FK
    seller_of_product = Relationship('DbUser', back_populates='prod_items')
    product_orders = Relationship('DbOrder', back_populates='ordered_product')

class DbUser(Base):
    __tablename__= "user"
    id = Column(Integer, primary_key=True, index=True) #PK
    fname = Column(String)
    lname = Column(String)
    email = Column(String)
    password = Column(String)
    is_admin = Column(Boolean)
    is_activate = Column(Boolean)
    creation_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime)
    buyer_orders = Relationship('DbOrder', back_populates='buyer_of_product')
    #sent_messages = Relationship('DbMessage', back_populates='sender')
    #received_messages = Relationship('DbMessage', back_populates='receiver')
    created_catgories = Relationship('DbCategory', back_populates='owner_admin')
    prod_items = Relationship('DbProduct', back_populates='seller_of_product')

class DbOrder(Base):
    __tablename__="order"
    id = Column(Integer, primary_key=True, index= True)
    product_id = Column(Integer, ForeignKey('product.id')) #FK
    ordered_product = Relationship('DbProduct', back_populates='product_orders')
    buyer_id = Column(Integer, ForeignKey('user.id')) #FK
    buyer_of_product = Relationship('DbUser', back_populates='buyer_orders')
    status = Column(Integer) #0: Ordered, 1: Shipped, 2: Delivered, 3: Returned, 4: Cancelled
    quantity = Column(Integer)
    total_price = Column(Float)
    is_activate = Column(Boolean)
    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    related_invoice = Relationship('DbInvoice', back_populates='products_per_invoice')
    creation_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime)
    updated_status_timestamp = Column(DateTime)

class DbInvoice(Base):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True, index=True)
    creation_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime)
    payment_mehtod = Column(Integer)#0: Paybal, 1: DebitCard, 2: CreditCard..
    total_price = Column(Float)
    barcode_url = Column(String)
    products_per_invoice = Relationship('DbOrder', back_populates='related_invoice')

class DbMessage(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('user.id'))
    sender = Relationship('DbUser', foreign_keys=[sender_id])
    receiver_id = Column(Integer, ForeignKey('user.id'))
    receiver = Relationship('DbUser', foreign_keys=[receiver_id])
    msg_txt = Column(String)
    msg_status = Column(Integer) #0: sent, 1: received, 2: read, 3: deleted
    creation_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime)
