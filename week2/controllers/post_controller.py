import httpx
from fastapi import HTTPException, Query
from sqlmodel import select
from typing import Annotated

from database import SessionDep
from models.post_model import Post

# 게시물 작성
def create_post(post: Post, session: SessionDep) -> Post:
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

# 게시물 전체 읽기
def read_posts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Post]:
    posts = session.exec(
        select(Post).offset(offset).limit(limit)
    ).all()

    return posts

# 특정 게시물 읽기
def read_post(post_id: int, session: SessionDep) -> Post:
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post

# 게시물 수정
def update_post(post_id: int, update_post: Post, session: SessionDep) -> Post:
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = update_post.title
    post.content = update_post.content
    post.name = update_post.name

    session.add(post)
    session.commit()
    session.refresh(post)

    return post

# 게시물 삭제
def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()

    return {"ok": True}

# ollama로 게시물 요약
def summarize_post(post_id: int, session: SessionDep) -> dict:
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    payload = {
        "model": "gemma4:e4b",
        "messages": [
            {
                "role": "system",
                "content": "당신은 커뮤니티 게시글을 요약하는 친절한 AI 어시스턴트입니다."
            },
            {
                "role": "user",
                "content": f"다음 게시글을 한국어로 3줄 이내로 요약해줘:\n\n{post.content}"
            },
        ],
    }

    response = httpx.post(
        "http://localhost:11434/v1/chat/completions",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=60.0,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Ollama summary failed")

    result = response.json()

    return {
        "post_id": post.id,
        "summary": result["choices"][0]["message"]["content"]
    }