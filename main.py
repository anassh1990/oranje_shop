from fastapi import FastAPI
from database import models
from database.database import engine
from routers import category
from routers import product
from routers import user
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(category.router)
app.include_router(product.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')