from fastapi import APIRouter, status, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from pydantic import EmailStr
from blog_api import models, schemas, hashing, jwt
import database
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Login"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Token)
def user_login(email: EmailStr = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    exist_user = db.query(models.User).filter(
        models.User.email == email).first()
    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")

    if not hashing.verify_password(password, exist_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="input is invalid")

    jw_token = jwt.create_access_token({"email": exist_user.email})
    return jw_token
