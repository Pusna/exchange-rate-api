from sqlalchemy import Column, Integer, String
from exchange_rate.database import Base


class Subscriber(Base):
    __tablename__ = "subs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)