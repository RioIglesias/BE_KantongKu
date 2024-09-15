from sqlmodel import SQLModel, Field, Relationship, TIMESTAMP, Column, text
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.users_model import User
    from .income_p_model import IncomePersonal


class CategoryIncomeBase(SQLModel):
    name: str = Field(default=None)


class CreateCategory(CategoryIncomeBase):
    created_by: int


class CategoryIncomePublic(CategoryIncomeBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime | None = None


class CategoryIncomePersonal(CategoryIncomeBase, table=True):
    __tablename__ = "category_income_personal"

    id: int = Field(default=None, primary_key=True)
    created_by: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
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
    user: Optional["User"] = Relationship(back_populates="income_personal_category")
    income_category_personal: Optional["IncomePersonal"] = Relationship(
        back_populates="category"
    )


# income_category_personal_fkey