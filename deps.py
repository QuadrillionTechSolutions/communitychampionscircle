from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from auth import decode_jwt
from models import User

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    uid = decode_jwt(authorization.split(" ",1)[1])
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.get(User, uid)
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive or missing user")
    return user

def get_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user
