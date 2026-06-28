from app.database.base import Base
from app.database.engine import engine
from app.database.session import SessionLocal, get_db

def create_tables():
    from app.domains.auth.models import User
    from app.domains.posts.models import Post
    
    Base.metadata.create_all(bind=engine)

__all__ = ["Base", "engine", "SessionLocal", "get_db", "create_tables"]
