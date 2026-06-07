from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from datetime import date

from app.database import get_db
from app.models import Customer

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=302)

    today = date.today()

    total_customers = db.query(Customer).count()

    today_records = (
        db.query(Customer)
        .filter(Customer.call_date == today)
        .all()
    )

    today_total_calls = sum(
        customer.total_calls
        for customer in today_records
    )

    today_closed_calls = sum(
        customer.closed_calls
        for customer in today_records
    )

    today_pending_calls = (
        today_total_calls -
        today_closed_calls
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": request.session["user"],
            "total_customers": total_customers,
            "today_total_calls": today_total_calls,
            "today_closed_calls": today_closed_calls,
            "today_pending_calls": today_pending_calls
        }
    )