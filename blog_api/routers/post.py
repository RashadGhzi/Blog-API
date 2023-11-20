from fastapi import APIRouter, status, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
import database
from typing import List
from blog_api import models, schemas, oauth
import file_upload
import os

router = APIRouter(tags=["Post"])

# functionality for posting blog
@router.post("/post_blog", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReponse)
def post_blog(
    title: str = Form(...),
    content: str = Form(...),
    file_data: UploadFile = File(None),
    db: Session = Depends(database.get_db),
    current_user_email: str = Depends(oauth.get_current_user),
):
    try:
        file_path = file_upload.file_or_image_upload("blog",file_data)
        new_post = models.Post(
            title=title,
            content=content,
            file=file_path,
            user_email=current_user_email.email,
        )

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        print(new_post)
        return new_post

    except Exception as e:
        # Catch any exceptions and return a 400 Bad Request with the error message
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

# functionality for getting all post
@router.get("/get_blogs", status_code=status.HTTP_200_OK, response_model=List[schemas.PostReponse])
def get_blogs(db: Session = Depends(database.get_db), current_user_email: str = Depends(oauth.get_current_user)):
    try:

        all_blog_post = db.query(models.Post).filter(
            models.Post.user_email == current_user_email.email)
        return all_blog_post
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

# functionality for deleting post
@router.delete("/delete_blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(database.get_db), current_user_email: str = Depends(oauth.get_current_user)):
    blog = db.query(models.Post).filter(models.Post.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="post not found")
    if blog.user_email != current_user_email.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    db.delete(blog)
    # deleting file directory 
    folder_dir = os.path.join(os.getcwd(), f"uploads/{blog.file}")
    if os.path.exists(folder_dir):
        os.remove(folder_dir)
    db.commit()
    return "delete blogs"

# functionality for updating post
@router.put("/update_blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostReponse)
def update_blog(id: int, title: str = Form(None), content: str = Form(None), file: UploadFile = File(None), db: Session = Depends(database.get_db), current_user_email: str = Depends(oauth.get_current_user)):
    blog = db.query(models.Post).filter(models.Post.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="post not found")
    if blog.user_email != current_user_email.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    if title:
        print(title)
        blog.title = title
    if content:
        blog.content = content
    if file:
        # deleting file directory 
        folder_dir = os.path.join(os.getcwd(), f"uploads/{blog.file}")
        if os.path.exists(folder_dir):
            os.remove(folder_dir)
        file_path = file_upload.file_or_image_upload("blog",file)
        blog.file = file_path

    db.commit()
    return blog
