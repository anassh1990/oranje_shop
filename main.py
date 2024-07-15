from fastapi import FastAPI
from database import models
from database.database import engine
from routers import category, product, user, order
from auth import authentication
from fastapi.staticfiles import StaticFiles
from auth import authentication


app = FastAPI()
app.include_router(category.router)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(order.router)
models.Base.metadata.create_all(engine)
app.mount('/images', StaticFiles(directory='images'), name='images')