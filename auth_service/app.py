from fastapi import FastAPI
from auth_service.routes import auth_router
from auth_service.database import create_db_and_tables, disconnect_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.on_event("shutdown")
async def on_shutdown():
    await disconnect_db()


app.include_router(
    auth_router,
    prefix="/auth"
)
