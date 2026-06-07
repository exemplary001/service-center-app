from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(100), nullable=False)

    address = Column(String(500))

    phone_number = Column(String(20))

    call_date = Column(Date)

    total_calls = Column(Integer, default=0)

    closed_calls = Column(Integer, default=0)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(50),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )