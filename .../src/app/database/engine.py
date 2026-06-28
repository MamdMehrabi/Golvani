from sqlalchemy import create_engine

from app.core.configs import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
