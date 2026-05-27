_users = [
    {"user_id": 1, "name": "Alice", "email": "alice@test.com"},
    {"user_id": 2, "name": "Bob", "email": "bob@test.com"},
    {"user_id": 3, "name": "Carol", "email": "carol@test.com"},
]

# 모든 사용자 조회
def get_users():
    return _users.copy()  # 외부에서 수정 방지

# ID로 사용자 조회
def get_user_by_id(user_id: int):
    for user in _users:
        if user["user_id"] == user_id:
            return user

    return None

# 이메일로 사용자 조회
def get_user_by_email(email: str):
    for user in _users:
        if user["email"] == email:
            return user

    return None

# 새 사용자 추가
def add_user(user: dict):
    _users.append(user)
    return user

# 사용자 탈퇴
def remove_user(user_id: int):
    for user in _users:
        if user["user_id"] == user_id:
            _users.remove(user)
            return user["user_id"]

    return None