from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timedelta
from collections import Counter

app = FastAPI()

# Sample database as a list
products_db = []
orders_db = []
#users_db = [["1","goitom","try@gmail.com","false"],["2","gdey","try1@gmail.com","false"]]
users_db = []
user_activity_db = []

# Models
class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    price: float
    stock: int

class Order(BaseModel):
    id: Optional[str] = None
    product_id: str
    quantity: int
    total_price: Optional[float] = None
    timestamp: datetime = datetime.now()

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    is_admin: bool
    activity: List[str] = []

class UserActivity(BaseModel):
    user_id: str
    activity: str
    timestamp: datetime = datetime.now()

#New for KPI reporting system
class KPIReport(BaseModel):
    total_users: int
    total_orders: int
    total_revenue: float
    average_order_value: float
    total_products: int
    products_out_of_stock: int

# Admin authentication dependency when user login
def get_current_admin_user():
    # admin authentication
    user = User(id=str(uuid4()), username="admin", email="admin@example.com", is_admin=True)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

# Endpoints for products
@app.post("/products/", response_model=Product, tags=['Product'])
def create_product(product: Product, admin_user: User = Depends(get_current_admin_user)):
    product.id = str(uuid4())
    products_db.append(product.dict())
    return product

@app.get("/products/", response_model=List[Product], tags=['Product'])
def list_products(admin_user: User = Depends(get_current_admin_user)):
    return products_db

@app.get("/products/{product_id}", response_model=Product, tags=['Product'])
def get_product(product_id: str, admin_user: User = Depends(get_current_admin_user)):
    product = next((prod for prod in products_db if prod["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=Product, tags=['Product'])
def update_product(product_id: str, product: Product, admin_user: User = Depends(get_current_admin_user)):
    for prod in products_db:
        if prod["id"] == product_id:
            prod.update(product.dict(exclude_unset=True))
            return prod
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", tags=['Product'])
def delete_product(product_id: str, admin_user: User = Depends(get_current_admin_user)):
    global products_db
    products_db = [prod for prod in products_db if prod["id"] != product_id]
    return {"detail": "Product deleted"}

@app.get("/orders/", response_model=List[Order], tags=['Order'])
def list_orders(admin_user: User = Depends(get_current_admin_user)):
    return orders_db

@app.get("/users/", response_model=List[User], tags=['User'])
def list_users(admin_user: User = Depends(get_current_admin_user)):
    return users_db

@app.get("/users/{user_id}", response_model=User, tags=['User'])
def get_user(user_id: str, admin_user: User = Depends(get_current_admin_user)):
    user = next((usr for usr in users_db if usr["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User, tags=['User'])
def update_user(user_id: str, user: User, admin_user: User = Depends(get_current_admin_user)):
    for usr in users_db:
        if usr["id"] == user_id:
            usr.update(user.dict(exclude_unset=True))
            return usr
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", tags=['User'])
def delete_user(user_id: str, admin_user: User = Depends(get_current_admin_user)):
    global users_db
    users_db = [usr for usr in users_db if usr["id"] != user_id]
    return {"detail": "User deleted"}

# Reporting Endpoints
@app.get("/reports/user-activity/", tags=['Report'])
def user_activity_report(admin_user: User = Depends(get_current_admin_user)):
    activity_count = Counter([activity["activity"] for activity in user_activity_db])
    return activity_count

@app.get("/reports/sales/", tags=['Report'])
def sales_report(admin_user: User = Depends(get_current_admin_user)):
    total_sales = sum(order["total_price"] for order in orders_db)
    product_sales = Counter([order["product_id"] for order in orders_db])
    top_selling_products = product_sales.most_common()
    return {
        "total_sales": total_sales,
        "top_selling_products": top_selling_products
    }

@app.get("/reports/platform-performance/", tags=['Report'])
def platform_performance_report(admin_user: User = Depends(get_current_admin_user)):
    active_users = len(users_db)
    total_sales = sum(order["total_price"] for order in orders_db)
    sales_last_30_days = sum(
        order["total_price"]
        for order in orders_db
        if order["timestamp"] >= datetime.now() - timedelta(days=30)
    )
    return {
        "active_users": active_users,
        "total_sales": total_sales,
        "sales_last_30_days": sales_last_30_days
    }



@app.get("/reports/kpis/", response_model=KPIReport, tags=['KPI reporting'])
def kpi_report(admin_user: User = Depends(get_current_admin_user)):
    total_users = len(users_db)
    total_orders = len(orders_db)
    total_products = len(products_db)
    
    return KPIReport(
        total_users=total_users,
        total_orders=total_orders,
        total_products=total_products,      
    )