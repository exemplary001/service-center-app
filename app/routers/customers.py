from fastapi import APIRouter
from fastapi import Request
from fastapi import Form
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File

import pandas as pd
import tempfile

from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import or_

from datetime import datetime

from app.database import get_db
from app.models import Customer

from app.services.excel_export import generate_excel

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/customers")
def customers(
    request: Request,
    page: int = 1,
    search: str = "",
    db: Session = Depends(get_db)
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=302)

    per_page = 10

    query = db.query(Customer)

    if search:
        query = query.filter(
            or_(
                Customer.customer_name.ilike(f"%{search}%"),
                Customer.phone_number.ilike(f"%{search}%")
            )
        )

    total_records = query.count()

    customers = (
        query.order_by(Customer.id.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    total_pages = max(
        (total_records + per_page - 1) // per_page,
        1
    )

    return templates.TemplateResponse(
        "customers.html",
        {
            "request": request,
            "customers": customers,
            "page": page,
            "total_pages": total_pages,
            "search": search,
            "edit_customer": None
        }
    )


@router.post("/customers/add")
def add_customer(
    customer_name: str = Form(...),
    address: str = Form(...),
    phone_number: str = Form(...),
    call_date: str = Form(...),
    total_calls: int = Form(...),
    closed_calls: int = Form(...),
    db: Session = Depends(get_db)
):

    customer = Customer(
        customer_name=customer_name,
        address=address,
        phone_number=phone_number,
        call_date=datetime.strptime(
            call_date,
            "%Y-%m-%d"
        ).date(),
        total_calls=total_calls,
        closed_calls=closed_calls
    )

    db.add(customer)
    db.commit()

    return RedirectResponse(
        "/customers",
        status_code=303
    )


@router.get("/customers/edit/{customer_id}")
def edit_customer(
    customer_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=302)

    customers = (
        db.query(Customer)
        .order_by(Customer.id.desc())
        .all()
    )

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    return templates.TemplateResponse(
        "customers.html",
        {
            "request": request,
            "customers": customers,
            "edit_customer": customer,
            "page": 1,
            "total_pages": 1,
            "search": ""
        }
    )


@router.post("/customers/update/{customer_id}")
def update_customer(
    customer_id: int,
    customer_name: str = Form(...),
    address: str = Form(...),
    phone_number: str = Form(...),
    call_date: str = Form(...),
    total_calls: int = Form(...),
    closed_calls: int = Form(...),
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if customer:

        customer.customer_name = customer_name
        customer.address = address
        customer.phone_number = phone_number

        customer.call_date = datetime.strptime(
            call_date,
            "%Y-%m-%d"
        ).date()

        customer.total_calls = total_calls
        customer.closed_calls = closed_calls

        db.commit()

    return RedirectResponse(
        "/customers",
        status_code=303
    )


@router.get("/customers/delete/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if customer:
        db.delete(customer)
        db.commit()

    return RedirectResponse(
        "/customers",
        status_code=303
    )


@router.get("/customers/export")
def export_excel(
    db: Session = Depends(get_db)
):

    customers = (
        db.query(Customer)
        .order_by(Customer.id.desc())
        .all()
    )

    filename = generate_excel(customers)

    return FileResponse(
        filename,
        filename=filename
    )

@router.post("/customers/import")
async def import_excel(
    excel_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".xlsx"
    )

    contents = await excel_file.read()

    temp_file.write(contents)

    temp_file.close()

    try:

        df = pd.read_excel(
            temp_file.name
        )

        for _, row in df.iterrows():

            try:

                customer_name = str(
                    row["NAME"]
                ).strip()

                address = str(
                    row["ADDRESS"]
                ).strip()

                phone_number = str(
                    row["MOBILE NUMBER"]
                ).strip()

                call_date = pd.to_datetime(
                    row["DATE"]
                ).date()

                total_calls = int(
                    row["OVERALL CALL"]
                )

                closed_calls = int(
                    row["CLOSED CALL"]
                )

                existing = (
                    db.query(Customer)
                    .filter(
                        Customer.customer_name == customer_name,
                        Customer.phone_number == phone_number
                    )
                    .first()
                )

                if existing:
                    continue

                customer = Customer(
                    customer_name=customer_name,
                    address=address,
                    phone_number=phone_number,
                    call_date=call_date,
                    total_calls=total_calls,
                    closed_calls=closed_calls
                )

                db.add(customer)

            except Exception:
                continue

        db.commit()

    except Exception as e:

        print(
            "Import Error:",
            str(e)
        )

    return RedirectResponse(
        "/customers",
        status_code=303
    )