from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import select

from database import SessionDep
from models.user_model import User


class LoginRequest(BaseModel):
    email: str

# 유저 전체 검색
def get_users(session: SessionDep) -> list[User]:
    users = session.exec(select(User)).all()
    return users

# 특정 유저 검색
def get_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# 유저 생성
def create_user(user: User, session: SessionDep) -> User:
    exist_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if exist_user:
        raise HTTPException(status_code=409, detail="Email already exists")

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

# 로그인
def login(request: LoginRequest, session: SessionDep) -> dict:
    user = session.exec(
        select(User).where(User.email == request.email)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }

# 유저 삭제
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"ok": True}