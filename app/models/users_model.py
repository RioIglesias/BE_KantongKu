from sqlmodel import SQLModel, Field, Relationship, Column, TIMESTAMP, text
from typing import List
from datetime import datetime, timezone

from .personal.income.income_p_model import IncomePersonal
from .personal.income.category_p_i_model import CategoryIncomePersonal
from .personal.income.images_p_i_model import ImagesIncomePersonal


class UserBase(SQLModel):
    name: str = Field(min_length=3, max_length=20)
    username: str = Field(unique=True, min_length=5, max_length=25)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str
    created_at: datetime | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP"),
        )
    )
    income_personal: List["IncomePersonal"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    income_personal_category: List["CategoryIncomePersonal"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    income_personal_images: List["ImagesIncomePersonal"] = Relationship(
        back_populates="user", cascade_delete=True
    )


print(datetime.now().tzname)


class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=25)


class UserUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=3, max_length=20)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=4, max_length=25)
    new_password: str = Field(min_length=4, max_length=25)


class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
