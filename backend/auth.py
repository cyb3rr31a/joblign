from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal
from dotenv import load_dotenv
import models
import os

# Load environment variables
load_dotenv()

# Variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

if not SECRET_KEY:
   raise ValueError("SECRET_KEY is not set in the environment")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
      db.close()

def hash_password(password: str):
   return pwd_context.hash(password)

def verify_password(plain, hashed):
   return pwd_context.verify(plain, hashed) 

def create_access_token(data: dict, expires_delta=None):
   to_encode = data.copy()
   expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({"exp": expire})
   if not SECRET_KEY:
      raise ValueError("SECRET_KEY is not set in the environment")
   return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
      status_code=401, 
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )
    if not SECRET_KEY:
       raise ValueError("SECRET_KEY is not set in the environment")
    
    try:
       payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
       user_id = payload.get("sub")
       if user_id is None:
          raise credentials_exception
      
    except JWTError:
       raise credentials_exception
   
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
       raise credentials_exception
    return user
   
