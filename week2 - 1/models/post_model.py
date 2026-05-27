_posts = [
    {"post_id" : 1, "name": "Alice", "title" : "제목1", "contents" : "안녕하세요"},
    {"post_id" : 2, "name": "Bob", "title" : "제목2", "contents" : "안녕하세요1"},
    {"post_id" : 3, "name": "Carol", "title" : "제목3", "contents" : "안녕하세요2"}
]

# 모든 게시물 조회
def get_posts():
    return _posts.copy()  # 외부에서 수정 방지

# ID로 게시물 조회
def get_post_by_id(post_id: int):
    for post in _posts:
        if post["post_id"] == post_id:
            return post

    return None

# 내 게시물 조회
def get_post_by_name(name: str):
    posts = []
    for post in _posts:
        if post["name"] == name:
            posts.append(post)

    if len(posts) == 0:
        return None

    return posts

# 새 게시물 추가
def add_post(post: dict):
    _posts.append(post)
    return post

# 게시물 수정
def update_post(post_id: int, data: dict):
    post = get_post_by_id(post_id)

    if post is None:
        return None

    post.update(data)
    return post

# 게시물 삭제
def remove_post(post_id: int):
    post = get_post_by_id(post_id)

    if post is None:
        return None

    _posts.remove(post)
    return post_id