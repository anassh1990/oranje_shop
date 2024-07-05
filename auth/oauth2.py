from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
# import secrets
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from database.database import get_db
from fastapi import HTTPException,status
from jose.exceptions import JWTError
from database import db_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#def generate_secret_key(length=32):
#    return secrets.token_hex(length)

SECRET_KEY = 'f458a1f1455aa72b3a20beac7b0d2bd080ff270eab8f403c07283e422ae341c8'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str= Depends(oauth2_scheme), db: Session = Depends(get_db)):
   credentials_exception = HTTPException(
      status_code= status.HTTP_401_UNAUTHORIZED,
      detail= 'Could not validate credentials',
      headers={"WWW-Authenticate": "Bearer"}
   )
   try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      username: str = payload.get("username")
      if username is None:
         raise credentials_exception
   except JWTError:
      raise credentials_exception
   user = db_user.get_user_by_username(db, username)

   if user is None:
      raise credentials_exception
   return user





