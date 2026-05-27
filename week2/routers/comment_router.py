from fastapi import APIRouter

from controllers import comment_controller
from database import SessionDep
from models.comment_model import Comment

router = APIRouter(tags=["comments"])


@router.post("/posts/{post_id}/comments/")
def create_comment(post_id: int, comment: Comment, session: SessionDep) -> Comment:
    return comment_controller.create_comment(post_id, comment, session)


@router.get("/posts/{post_id}/comments/")
def read_comments(post_id: int, session: SessionDep) -> list[Comment]:
    return comment_controller.read_comments(post_id, session)


@router.get("/comments/{comment_id}")
def read_comment(comment_id: int, session: SessionDep) -> Comment:
    return comment_controller.read_comment(comment_id, session)


@router.patch("/comments/{comment_id}")
def update_comment(comment_id: int, comment: Comment, session: SessionDep) -> Comment:
    return comment_controller.update_comment(comment_id, comment, session)


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, session: SessionDep):
    return comment_controller.delete_comment(comment_id, session)


@router.get("/comments/{comment_id}/summary")
def summarize_comment(comment_id: int, session: SessionDep) -> dict:
    return comment_controller.summarize_comment(comment_id, session)