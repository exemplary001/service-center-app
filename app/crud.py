from sqlalchemy.orm import Session

from app.models import Customer


def get_customers(
    db: Session,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Customer)
        .order_by(Customer.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_customer(
    db: Session,
    customer
):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(
    db: Session,
    customer_id: int
):
    return (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )


def update_customer(
    db: Session,
    customer,
    data
):
    customer.customer_name = data.customer_name
    customer.address = data.address
    customer.phone_number = data.phone_number
    customer.call_date = data.call_date
    customer.total_calls = data.total_calls
    customer.closed_calls = data.closed_calls

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(
    db: Session,
    customer
):
    db.delete(customer)
    db.commit()