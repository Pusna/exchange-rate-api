from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth_service.schemas import UserCreate, Token, UserLogin
from auth_service.models import User
from auth_service.auth import hash_password, verify_password, create_access_token
from auth_service.database import SessionLocal, get_db
from fastapi import Request

from jose import jwt, JWTError
from dotenv import load_dotenv
import os

auth_router = APIRouter()

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'


@auth_router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Користувач вже існує")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    await db.commit()

    return {"message": "Користувача успішно зареєстровано"}


@auth_router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Невірний email або пароль")

    token = create_access_token({
        "sub": user.email,
        "id": user.id,
        "username": user.username
    })

    return {"access_token": token, "token_type": "bearer"}
