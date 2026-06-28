from sqlalchemy import Column, Integer, String

from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    content = Column(String)
    time = Column(String)
