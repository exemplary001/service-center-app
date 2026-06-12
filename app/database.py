from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def get_database_url():
    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///database/service_center.db"
    )

    if not database_url.startswith("sqlite:///"):
        return database_url

    database_path = database_url.replace(
        "sqlite:///",
        "",
        1
    )

    if database_path == ":memory:":
        return database_url

    path = Path(database_path)

    if not path.is_absolute():
        path = BASE_DIR / path

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return f"sqlite:///{path.as_posix()}"


DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
