from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)


def register_user(db: Session, user):
    if get_user_by_email(db, user.email):
        raise Exception("Email already registered")

    if get_user_by_username(db, user.username):
        raise Exception("Username already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    return create_user(db, new_user)