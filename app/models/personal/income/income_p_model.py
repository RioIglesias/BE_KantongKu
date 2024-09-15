from sqlmodel import SQLModel, Field, Relationship, TIMESTAMP, Column, text
from decimal import Decimal
from datetime import datetime, date
from typing import TYPE_CHECKING, Optional, List
from .images_p_i_model import CreateImagesIncomePersonal, ImageRead

if TYPE_CHECKING:
    from ...users_model import User
    from .category_p_i_model import CategoryIncomePersonal
    from .images_p_i_model import ImagesIncomePersonal



class IncomePersonalBase(SQLModel):
    title: str = Field(min_length=3, max_length=25)
    amount: Decimal = Field(default=0, decimal_places=2)
    desc: str | None
    date: date

class CreateIncomePersonal(IncomePersonalBase):
    category_id: int
    desc: str | None = None
    images: list["CreateImagesIncomePersonal"] | None = None

class IncomePublic(IncomePersonalBase):
    id: int
    category_name: str
    images: list["ImageRead"] | None = None

class IncomePersonal(IncomePersonalBase, table=True):
    __tablename__ = "income_personal"
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=25)
    category_id: int = Field(
        foreign_key="category_income_personal.id", ondelete="SET NULL", nullable=True
    )
    category_name: str
    desc: str | None
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
    user: Optional["User"] = Relationship(back_populates="income_personal")
    category: Optional["CategoryIncomePersonal"] = Relationship(
        back_populates="income_category_personal"
    )
    images: Optional[List["ImagesIncomePersonal"]] = Relationship(
        back_populates="income_images_personal", sa_relationship_kwargs={'lazy': 'selectin'}
    )