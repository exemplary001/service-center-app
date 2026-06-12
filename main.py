from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from dotenv import load_dotenv
import os

from app.database import Base
from app.database import engine
from app.database import SessionLocal
from app.services.excel_import import import_sample_data

load_dotenv()

app = FastAPI(
    title="Service Center Call Tracker"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)

Base.metadata.create_all(bind=engine)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

from app.routers import auth
from app.routers import dashboard
from app.routers import customers
from app.routers import settings

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(customers.router)
app.include_router(settings.router)

@app.on_event("startup")
def load_sample_excel():

    if os.getenv("LOAD_SAMPLE_DATA", "false").lower() != "true":
        return

    db = SessionLocal()

    try:
        import_sample_data(db)

    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
