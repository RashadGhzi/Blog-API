from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from blog_api.routers import user, auth, post
import database
from blog_api import models



models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(post.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
