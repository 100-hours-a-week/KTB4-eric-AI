from fastapi import FastAPI
from routers.user_router import router as user_router
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}