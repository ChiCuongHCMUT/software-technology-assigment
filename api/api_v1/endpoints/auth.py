from fastapi import APIRouter, Header
from models.user import CreateUserRequest


router = APIRouter(prefix="/auth")

@router.post(
    "/signup/admin",
)
async def create_admin_user(
    create_admin_user: CreateUserRequest
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e

@router.get(
    "/signin/admin",
)
async def signin_admin_user(
    user_name: str = Header(..., description="User Name"),
    password: str = Header(..., description="Password"),
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e


@router.get(
    "/signin/student",
)
async def signin_student_user(
):
    try:
        # Todo
        pass
    except Exception as e:
        raise e