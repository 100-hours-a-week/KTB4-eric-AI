from typing import Annotated

from fastapi import APIRouter, Query

from controllers import post_controller
from database import SessionDep
from models.post_model import Post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/")
def create_post(post: Post, session: SessionDep) -> Post:
    return post_controller.create_post(post, session)


@router.get("/")
def read_posts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Post]:
    return post_controller.read_posts(session, offset, limit)


@router.get("/{post_id}")
def read_post(post_id: int, session: SessionDep) -> Post:
    return post_controller.read_post(post_id, session)


@router.patch("/{post_id}")
def update_post(post_id: int, post: Post, session: SessionDep) -> Post:
    return post_controller.update_post(post_id, post, session)


@router.delete("/{post_id}")
def delete_post(post_id: int, session: SessionDep):
    return post_controller.delete_post(post_id, session)


@router.get("/{post_id}/summary")
def summarize_post(post_id: int, session: SessionDep) -> dict:
    return post_controller.summarize_post(post_id, session)