import httpx
from fastapi import HTTPException
from sqlmodel import select

from database import SessionDep
from models.post_model import Post
from models.comment_model import Comment

# 댓글 작성
def create_comment(post_id: int, comment: Comment, session: SessionDep) -> Comment:
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment.post_id = post_id

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment

# 전체 댓글 읽기
def read_comments(post_id: int, session: SessionDep) -> list[Comment]:
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = session.exec(
        select(Comment).where(Comment.post_id == post_id)
    ).all()

    return comments

# 댓글 읽기
def read_comment(comment_id: int, session: SessionDep) -> Comment:
    comment = session.get(Comment, comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment

# 댓글 수정
def update_comment(comment_id: int, update_comment: Comment, session: SessionDep) -> Comment:
    comment = session.get(Comment, comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.content = update_comment.content
    comment.name = update_comment.name

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment

# 댓글 삭제
def delete_comment(comment_id: int, session: SessionDep):
    comment = session.get(Comment, comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    session.delete(comment)
    session.commit()

    return {"ok": True}

