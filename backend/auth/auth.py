import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.schema import User
from dotenv import load_dotenv
from backend.auth.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, oauth2_scheme

# Load environment variables from the .env file
load_dotenv()

# Create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
