from fastapi import APIRouter

from controllers import user_controller
from database import SessionDep
from models.user_model import User
from controllers.user_controller import LoginRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(session: SessionDep) -> list[User]:
    return user_controller.get_users(session)


@router.get("/{user_id}")
def get_user(user_id: int, session: SessionDep) -> User:
    return user_controller.get_user(user_id, session)


@router.post("/")
def create_user(user: User, session: SessionDep) -> User:
    return user_controller.create_user(user, session)


@router.post("/login")
def login(request: LoginRequest, session: SessionDep) -> dict:
    return user_controller.login(request, session)



@router.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    return user_controller.delete_user(user_id, session)