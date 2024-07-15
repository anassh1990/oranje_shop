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
<<<<<<< HEAD
app.include_router(order.router)
=======
>>>>>>> 574b2e6a52f5f554a7e27407ca452bfb02315baa

models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')