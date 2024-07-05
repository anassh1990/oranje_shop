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
    parent_cat_id = mapped_column(Integer, ForeignKey('category.id')) #FK
    #parent_category = Relationship('DbCategory', back_populates='sub_cat_items')
    #sub_cat_items = Relationship('DbCategory', back_populates='parent_category', backref=)
    sub_cat_items = Relationship("DbCategory")
    prod_items = Relationship('DbProduct', back_populates='category_of_product')
    is_activate = mapped_column(Boolean) #True: activate to show, False: not activate to show
    admin_id = mapped_column(Integer) #FK
    

class DbProduct(Base):
    __tablename__= "product"
    id = Column(Integer, primary_key=True, index=True) #PK
    name = Column(String)
    image_url = Column(String)
    description = Column(Integer)
    rate = Column(Float)
    price = Column(Float)
    quantity = Column(Integer)
    status = Column(Integer) #0:soldout, 1:initiated, 2:approved by admin, 3:rejected by admin
    is_activate = Column(Boolean) #True: activate to show, False: not activate to show
    creation_timestamp = Column(DateTime)
    updated_status_timestamp = Column(DateTime)
    cat_id = Column(Integer, ForeignKey('category.id')) #FK
    category_of_product = Relationship('DbCategory', back_populates='prod_items')
    seller_id = Column(Integer, ForeignKey('user.id')) #FK
    seller_of_product = Relationship('DbUser', back_populates='prod_items')

class DbUser(Base):
    __tablename__= "user"
    id = Column(Integer, primary_key=True, index=True) #PK
    fname = Column(String)
    lname = Column(String)
    email = Column(String)
    password = Column(String)
    is_admin = Column(Boolean)
    creation_timestamp = Column(DateTime)
    prod_items = Relationship('DbProduct', back_populates='seller_of_product')

