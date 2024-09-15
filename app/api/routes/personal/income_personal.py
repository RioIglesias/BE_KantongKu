import io
from fastapi import APIRouter, HTTPException, UploadFile, File, status
from typing import Any

from fastapi.responses import JSONResponse, StreamingResponse
from app.core.db import session as get_session
from app.controllers import users_controller
from app.controllers.personal import income_p_controller
from app.models.personal.income.category_p_i_model import (
    CategoryIncomePersonal as Category,
    CreateCategory as CreateCategory,
    CategoryIncomePublic as CategoryPublic,
)
from app.models.personal.income.income_p_model import (
    CreateIncomePersonal,
    IncomePersonal,
    IncomePublic,
)
from app.helper.validation_images import validation_images



router = APIRouter()


@router.post("/images")
async def create_upload_file(session: get_session, file: UploadFile):
    validation_images(file=file)

    content = await file.read()
    db_image = await income_p_controller.create_test(
        session=session, filename=file.filename, content=content
    )
    return {"id": db_image.id, "filename": db_image.filename}


@router.get("/images")
async def read_image(image_id: int, session: get_session):
    db_image = await income_p_controller.get_test(session=session, test_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return StreamingResponse(io.BytesIO(db_image.content), media_type="image/png")


@router.post("/create", response_model=CategoryPublic)
async def created_category(category_in: CreateCategory, session: get_session) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await users_controller.get_user_by_id(
        session=session, id=category_in.created_by
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Ga ada user",
        )
    # category_create = CreateCategory.model_validate(category_in)
    user = await income_p_controller.create_category(
        session=session, category_in=category_in
    )

    return user


@router.post("/create-income", response_model=IncomePublic)
async def created_income(income_in: CreateIncomePersonal, session: get_session) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await users_controller.get_user_by_id(
        session=session, id=income_in.created_by
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Ga ada user",
        )
    category = await income_p_controller.get_category_by_id(
        session=session, id=income_in.category_id
    )
    if not category:
        raise HTTPException(
            status_code=400,
            detail="Ga ada category",
        )
    income = await income_p_controller.create_income(
        session=session, income_in=income_in, name_category=category
    )
    
    return income
