from fastapi import APIRouter
from controllers import user_controller

router = APIRouter(prefix="/users")

#전체 사용자 목록 조회
@router.get("")
def get_users():
    return user_controller.get_users()

#특정 사용자 상세 조회
@router.get("/{user_id}")
def get_user(user_id: int):
    return user_controller.get_user(user_id)

#사용자 생성 (status_code 201)
@router.post("", status_code = 201)
def create_user(data:dict):
    return user_controller.create_user(data)

#로그인
@router.post("/login")
def login(data:dict):
    return user_controller.login(data)
