from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.jwt_handler import create_access_token
from app.database.session import get_db
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.user_service import (
    login_user,
    register_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return register_user(db, user)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        logged_in_user = login_user(
            db,
            user.username,
            user.password,
        )

        access_token = create_access_token(
            data={
                "sub": logged_in_user.username
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@router.get("/me")
def get_me(
    current_user: str = Depends(get_current_user)
):
    return {
        "username": current_user
    }