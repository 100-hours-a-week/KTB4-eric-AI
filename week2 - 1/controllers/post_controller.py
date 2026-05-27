from fastapi import HTTPException
from models import post_model
from starlette import status


#게시물 목록 조회
def get_posts():
    posts = post_model.get_posts()
    if not posts:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data":posts}

#특정 게시물 조회
def get_post(post_id:int):
    if post_id <= 0:
        raise HTTPException(status_code=404, detail="Invalid user id")

    post = post_model.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data":post}

# 내 게시물 조회
def get_posts_mine(name: str):
    posts = post_model.get_post_by_name(name)

    if not posts:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"data":posts}


#게시물 작성
def create_post(data:dict):
    name = data.get("name")
    title = data.get("title")
    contents = data.get("contents")

    new_post = {"post_id": len(post_model.get_posts()) + 1, "name": name, "title": title, "contents": contents}
    post_model.add_post(new_post)
    return {"data":new_post}

#게시물 수정
def update_post(post_id:int, data:dict):
    post = post_model.get_post_by_id(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_post = post_model.update_post(post_id)
    return {"data":updated_post}

def delete_post(post_id:int):
    post = post_model.get_post_by_id(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post_model.remove_post(post_id)

    return {"data":post}