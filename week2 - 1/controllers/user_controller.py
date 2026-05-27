from fastapi import HTTPException
from models import user_model
from starlette import status


#사용자 목록 조회
def get_users():
    users = user_model.get_users()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data":users}

#특정 사용자 상세 조회
def get_user(user_id:int):
    if user_id <= 0:
        raise HTTPException(status_code=404, detail="Invalid user id")

    user = user_model.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data":user}

#사용자 생성
def create_user(data:dict):
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        raise HTTPException(status_code=400, detail="Missing required field")

    if user_model.get_user_by_email(email):
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = {"user_id": len(user_model.get_users()) + 1, "name": name, "email": email}
    user_model.add_user(new_user)
    return {"data":new_user}

#로그인
def login(data:dict):
    email = data.get("email")

    if not email:
        raise HTTPException(status_code=400, detail="Missing email")

    user = user_model.get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"data": {"user_id" : user["user_id"], "name": user["name"]}}

# 탈퇴
def remove_user(data:dict):
    user = user_model.get_user_by_id(data["user_id"])

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.remove_user(user["user_id"])
    return {"data":user}