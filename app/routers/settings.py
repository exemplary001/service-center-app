from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.auth import hash_password
from app.database import get_db
from app.models import Customer
from app.models import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")


def require_login(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/", status_code=302)

    return None


@router.get("/settings")
def settings_page(
    request: Request,
    success: str = "",
    error: str = "",
    db: Session = Depends(get_db)
):

    redirect = require_login(request)

    if redirect:
        return redirect

    user = (
        db.query(User)
        .filter(User.username == request.session["user"])
        .first()
    )

    if not user:
        request.session.clear()
        return RedirectResponse("/", status_code=302)

    total_customers = db.query(Customer).count()

    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "user": user,
            "total_customers": total_customers,
            "success": success,
            "error": error
        }
    )


@router.post("/settings/account")
def update_account(
    request: Request,
    username: str = Form(...),
    password: str = Form(""),
    confirm_password: str = Form(""),
    db: Session = Depends(get_db)
):

    redirect = require_login(request)

    if redirect:
        return redirect

    username = username.strip()

    if not username:
        return RedirectResponse(
            "/settings?error=Username+is+required",
            status_code=303
        )

    if password and password != confirm_password:
        return RedirectResponse(
            "/settings?error=Passwords+do+not+match",
            status_code=303
        )

    user = (
        db.query(User)
        .filter(User.username == request.session["user"])
        .first()
    )

    if not user:
        request.session.clear()
        return RedirectResponse("/", status_code=302)

    existing_user = (
        db.query(User)
        .filter(User.username == username)
        .filter(User.id != user.id)
        .first()
    )

    if existing_user:
        return RedirectResponse(
            "/settings?error=Username+already+exists",
            status_code=303
        )

    user.username = username

    if password:
        user.password = hash_password(password)

    db.commit()

    request.session["user"] = username

    return RedirectResponse(
        "/settings?success=Account+updated",
        status_code=303
    )


@router.post("/settings/clear-database")
def clear_database(
    request: Request,
    confirmation: str = Form(...),
    db: Session = Depends(get_db)
):

    redirect = require_login(request)

    if redirect:
        return redirect

    if confirmation != "CLEAR":
        return RedirectResponse(
            "/settings?error=Type+CLEAR+to+confirm",
            status_code=303
        )

    db.query(Customer).delete()
    db.commit()

    return RedirectResponse(
        "/settings?success=Customer+database+cleared",
        status_code=303
    )
