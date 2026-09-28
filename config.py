import os

SQLITE = "sqlite:///project.db"


class Config:
    DEBUG = os.environ.get("FLASK_DEBUG") == "1"
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", SQLITE)

    CKEDITOR_PKG_TYPE = 'full'
