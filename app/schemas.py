from pydantic import BaseModel
from datetime import date


class CustomerCreate(BaseModel):
    customer_name: str
    address: str
    phone_number: str
    call_date: date
    total_calls: int
    closed_calls: int


class CustomerUpdate(BaseModel):
    customer_name: str
    address: str
    phone_number: str
    call_date: date
    total_calls: int
    closed_calls: int


class CustomerResponse(BaseModel):
    id: int
    customer_name: str
    address: str
    phone_number: str
    total_calls: int
    closed_calls: int

    class Config:
        from_attributes = True