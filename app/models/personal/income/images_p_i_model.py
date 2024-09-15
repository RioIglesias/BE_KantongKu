from sqlmodel import SQLModel, Field, Relationship, TIMESTAMP, Column, text
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...users_model import User
    from .income_p_model import IncomePersonal

class ImagesIncomePersonalBase(SQLModel):
    images: bytes


class CreateImagesIncomePersonal(ImagesIncomePersonalBase):
    created_by: int


class ImageRead(ImagesIncomePersonalBase):
    id: int
    income_id: int


class ImagesIncomePersonal(ImagesIncomePersonalBase, table=True):
    __tablename__ = "images_income_personal"

    id: int = Field(default=None, primary_key=True)
    income_id: int = Field(
        foreign_key="income_personal.id", nullable=False, ondelete="CASCADE"
    )
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
    user: Optional["User"] = Relationship(back_populates="income_personal_images")
    income_images_personal: Optional["IncomePersonal"] = Relationship(
        back_populates="images"
    )



