import random
from fastapi import APIRouter, Header, HTTPException, status
from models.user import CreateUserRequest
from models.user import User
from utils import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth")

@router.post(
    "/signup/admin",
)
async def create_admin_user(
    create_admin_user: CreateUserRequest
):
    try:
        existing = await User.find_one(User.user_name == create_admin_user.user_name)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = User(
            user_id=random.randint(1000000, 9999999),
            user_name=create_admin_user.user_name,
            email=create_admin_user.email,
            phone_number=create_admin_user.phone_number,
            password=hash_password(create_admin_user.password),
            role="admin",
        )
        await new_user.insert()
        return {"message": "Admin user created successfully"}
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
        user = await User.find_one(User.user_name == user_name, User.role == "admin")
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="User name or password is incorrect!")

        token = create_access_token(data={"sub": user.user_id, "role": user.role})
        return {"access_token": token, "token_type": "bearer"}
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