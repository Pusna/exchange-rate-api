from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from exchange_rate.database import SessionLocal
from exchange_rate.models import Subscriber

from exchange_rate.exchange import get_exchange_rate

from exchange_rate.dependencies import get_current_user
from exchange_rate.schemas import AuthUserResponse

sub_router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session


@sub_router.post("/subscribe")
async def subscribe(db: AsyncSession = Depends(get_db),
                    current_user: AuthUserResponse = Depends(get_current_user)):
    result = await db.execute(select(Subscriber).where(Subscriber.email == current_user.email))
    existing = result.scalar_one_or_none()

    if existing:
        return {"message": "Ви вже підписані!"}

    subscriber = Subscriber(email=current_user.email)
    db.add(subscriber)
    await db.commit()
    return {"message": "Підписка оформлена успішно"}


@sub_router.get("/rate")
async def read_rate(current_user: AuthUserResponse = Depends(get_current_user)):
    rate = await get_exchange_rate()
    return f"Поточний курс - {rate} UAH"
