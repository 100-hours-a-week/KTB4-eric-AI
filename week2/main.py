from fastapi import FastAPI

from database import create_db_and_tables
from routers.post_router import router as post_router
from routers.comment_router import router as comment_router

app = FastAPI(
    title="Community API",
    description="FastAPI 커뮤니티 백엔드 과제"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)


@app.get("/")
def root():
    return {"message": "Community API"}