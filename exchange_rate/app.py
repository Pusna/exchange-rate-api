from fastapi import FastAPI
from exchange_rate.routes import sub_router
from exchange_rate.database import create_db_and_tables
from fastapi_utils.tasks import repeat_every
from exchange_rate.tasks import send_daily_exchange_rate

app = FastAPI(title="Exchange_rate")


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.on_event("startup")
@repeat_every(seconds=300)
async def periodic_email_sender() -> None:
    await send_daily_exchange_rate()


@app.get("/")
async def root():
    return {"message": "Hello everyone"}

app.include_router(
    sub_router,
    tags=["sub"],
    prefix="/api"
)
