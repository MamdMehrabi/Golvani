from sqlalchemy.orm import Session

from app.domains.auth.models import User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, username: str, hashed_password: str, is_admin: bool = False) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def user_exists(self, username: str) -> bool:
        return self.get_user_by_username(username) is not None
