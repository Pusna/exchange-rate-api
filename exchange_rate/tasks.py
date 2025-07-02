from exchange_rate.database import SessionLocal
from sqlalchemy.future import select
from exchange_rate.models import Subscriber
from exchange_rate.exchange import get_exchange_rate
from exchange_rate.email_utils import send_email


async def send_daily_exchange_rate():
    async with SessionLocal() as session:
        result = await session.execute(select(Subscriber))
        subscribers = result.scalars().all()

        rate = await get_exchange_rate()
        message = f"Поточний курс долара (USD → UAH): {rate} UAH"

        for sub in subscribers:
            await send_email(to_email=sub.email, subject="Курс USD", content=message)
