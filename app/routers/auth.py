from fastapi import APIRouter
from fastapi import Request
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.auth import verify_password
from app.auth import hash_password

from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.on_event("startup")
def create_admin():

    db: Session = SessionLocal()

    admin = (
        db.query(User)
        .filter(
            User.username ==
            os.getenv("ADMIN_USERNAME")
        )
        .first()
    )

    if not admin:

        user = User(
            username=os.getenv("ADMIN_USERNAME"),
            password=hash_password(
                os.getenv("ADMIN_PASSWORD")
            )
        )

        db.add(user)
        db.commit()

    db.close()


@router.get("/")
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    db.close()

    if not user:
        return RedirectResponse(
            "/",
            status_code=302
        )

    if not verify_password(
        password,
        user.password
    ):
        return RedirectResponse(
            "/",
            status_code=302
        )

    request.session["user"] = username

    return RedirectResponse(
        "/dashboard",
        status_code=302
    )


@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        "/",
        status_code=302
    )