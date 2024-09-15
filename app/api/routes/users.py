from fastapi import APIRouter, HTTPException
from typing import Any
from app.core.db import session as get_session
from app.controllers import users_controller
from app.models.users_model import UserPublic, UserCreate, UserUpdate, Token


router = APIRouter()


@router.post("/signup", response_model=UserPublic)
async def register_user(user_in: UserCreate, session: get_session) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await users_controller.get_user_by_username(
        session=session, username=user_in.username
    )
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = await users_controller.create_user(session=session, user_create=user_create)
    return user


@router.patch("/update", response_model=UserPublic)
async def update_user(user_id: int, user_in: UserUpdate, session: get_session) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await users_controller.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="The user with this id does not exist in the system",
        )

    user = await users_controller.update_user(
        session=session, user_in=user_in, db_user=user
    )
    return user


@router.post("/signin", response_model=UserPublic)
async def update_user(user_id: int, user_in: UserUpdate, session: get_session) -> Any:
    """
    Login user.
    """
    user = await users_controller.authenticate(session=session, username=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="The user with this id does not exist in the system",
        )

    user = await users_controller.update_user(
        session=session, user_in=user_in, db_user=user
    )
    return user


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(user_id: int, session: get_session) -> Any:
    """
    Login user.
    """
    user = await users_controller.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="The user with this id does not exist in the system",
        )       
    return user
