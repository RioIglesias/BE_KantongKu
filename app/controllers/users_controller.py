from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from sqlmodel import select
from app.core.security import get_password_hash, verify_password
from app.models.users_model import User, UserCreate, UserUpdate


async def create_user(*, session: AsyncSession, user_create: UserCreate) -> User:
    db_obj = User(
        name=user_create.name,
        username=user_create.username,
        password=get_password_hash(user_create.password),
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_user(
    *, session: AsyncSession, db_user: User, user_in: UserUpdate
) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_id(*, session: AsyncSession, id: int) -> User | None:
    statement = await session.execute(select(User).where(User.id == id))
    result = statement.scalars().first()
    return result


async def get_user_by_username(*, session: AsyncSession, username: str) -> User | None:
    statement = await session.execute(select(User).where(User.username == username))
    result = statement.scalars().first()
    return result


# async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
#     statement = await session.execute(select(User).where(User.email == email))
#     result = statement.scalars().first()
#     return result


async def authenticate(
    *, session: AsyncSession, username: str, password: str
) -> User | None:
    db_user = await get_user_by_username(session=session, username=username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
