import database
from blog_api import models, schemas
from fastapi import APIRouter, status, Depends, UploadFile, Form, File
from pydantic import EmailStr
from sqlalchemy.orm import Session
from blog_api import hashing, oauth
from fastapi import HTTPException
from file_upload import file_or_image_upload

router = APIRouter(tags=["User"])


@router.post("/user_create", status_code=status.HTTP_201_CREATED)
async def user_create(full_name:str=Form(...), email:EmailStr=Form(...), password:str=Form(...), avatar:UploadFile=File(None), db: Session = Depends(database.get_db)):
    try:
        hashed_password = hashing.get_password_hash(password)
        if avatar:
            file_path = file_or_image_upload("profile", avatar)
        else:
            file_path = None
        new_user = models.User(full_name=full_name,
                               email=email, hashed_password=hashed_password, avatar=file_path)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return "new user has been created"
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


# @router.get("/users_list", status_code=status.HTTP_200_OK, response_model=list[schemas.UserResponse])
# async def users_list(db: Session = Depends(database.get_db)):
#     try:
#         users = db.query(models.User).all()
#         return users
#     except Exception as error:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/user_details", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
async def user_details(db: Session = Depends(database.get_db), current_user_email: str = Depends(oauth.get_current_user)):
    try:
        current_user = current_user_email.email
        user = db.query(models.User).filter(
            models.User.email == current_user).first()
        return user
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
