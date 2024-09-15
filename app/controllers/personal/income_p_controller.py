from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from datetime import datetime
from sqlmodel import select
from app.models.personal.income.income_p_model import (
    CreateIncomePersonal,
    IncomePersonal,
)
from app.models.personal.income.images_p_i_model import (
    CreateImagesIncomePersonal,
    ImagesIncomePersonalBase,
    ImagesIncomePersonal,
)
from app.models.personal.income.category_p_i_model import (
    CreateCategory,
    CategoryIncomePersonal as category,
)
from fastapi import UploadFile

# from app.models.personal.income.income_p_model import CreateIncomePersonal as create_income


async def create_category(
    *, session: AsyncSession, category_in: CreateCategory
) -> category:
    db_category = category(name=category_in.name, created_by=category_in.created_by, )
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category


async def get_category_by_id(*, session: AsyncSession, id: int) -> category | None:
    statement = await session.execute(select(category).where(category.id == id))
    result = statement.scalars().first()
    return result


async def create_income(
    *, session: AsyncSession, income_in: CreateIncomePersonal, name_category: int
) -> IncomePersonal:
    db_income = IncomePersonal(
        title=income_in.title,
        category_id=income_in.category_id,
        category_name=name_category,
        amount=income_in.amount,
        desc=income_in.desc,
        date=income_in.date,
        created_by=income_in.created_by,
        created_at=income_in.created_at,
        updated_at=income_in.updated_at,
    )
    session.add(db_income)
    await session.commit()
    await session.refresh(db_income)
    if income_in.images:
        for images_data in income_in.images:
            db_images = ImagesIncomePersonal(
                images=images_data.images,
                income_id=db_income.id,
                created_by=db_income.created_by,
                created_at=images_data.created_at,
                updated_at=None,
            )
            session.add(db_images)
            await session.commit()
            await session.refresh(db_income)
    return db_income


#   db_income = IncomePersonal(
#         title=income_in.title,
#         category_id=income_in.category_id,
#         amount=income_in.amount,
#         desc=income_in.desc,
#         date=income_in.date,
#         created_by=income_in.created_by,
#         created_at=income_in.created_at,
#         updated_at=income_in.updated_at,
#     )

# async def create_test(*, session: AsyncSession, filename: str, content: bytes) -> test:
#     db_test = test(filename=filename, content=content)
#     session.add(db_test)
#     await session.commit()
#     await session.refresh(db_test)
#     return db_test


# async def get_test(*, session: AsyncSession, test_id: int) -> test:
#     statement = select(test).where(test.id == test_id)
#     result = await session.execute(statement)
#     return result.scalar_one_or_none()


# async def create_images(*, session: AsyncSession, user_create: UserCreate) -> User:
#     db_obj = User.model_validate(
#         user_create, update={"hashed_password": get_password_hash(user_create.password)}
#     )
#     session.add(db_obj)
#     await session.commit()
#     await session.refresh(db_obj)
#     return db_obj

# async def add_income(*, session: AsyncSession, user_create: UserCreate) -> User:
#     db_obj = User.model_validate(
#         user_create, update={"hashed_password": get_password_hash(user_create.password)}
#     )
#     session.add(db_obj)
#     await session.commit()
#     await session.refresh(db_obj)
#     return db_obj


# async def update_user(
#     *, session: AsyncSession, db_user: User, user_in: UserUpdate
# ) -> Any:
#     user_data = user_in.model_dump(exclude_unset=True)
#     extra_data = {}
#     if "password" in user_data:
#         password = user_data["password"]
#         hashed_password = get_password_hash(password)
#         extra_data["hashed_password"] = hashed_password
#     db_user.sqlmodel_update(user_data, update=extra_data)
#     session.add(db_user)
#     await session.commit()
#     await session.refresh(db_user)
#     return db_user


# async def get_user_by_id(*, session: AsyncSession, id: uuid.UUID) -> User | None:
#     statement = await session.execute(select(User).where(User.id == id))
#     result = statement.scalars().first()
#     return result


# async def get_user_by_username(*, session: AsyncSession, username: str) -> User | None:
#     statement = await session.execute(select(User).where(User.username == username))
#     result = statement.scalars().first()
#     return result
# # async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
# #     statement = await session.execute(select(User).where(User.email == email))
# #     result = statement.scalars().first()
# #     return result

# async def authenticate(
#     *, session: AsyncSession, username: str, password: str
# ) -> User | None:
#     db_user = await get_user_by_username(session=session, username=username)
#     if not db_user:
#         return None
#     if not verify_password(password, db_user.hashed_password):
#         return None
#     return db_user
