from sqlalchemy.orm import Session

from app.domains.auth.repository import AuthRepository
from app.domains.auth.usecases.hash_password import HashPassword
from app.common.exceptions import UserAlreadyExistsError


class RegisterUser:
    def __init__(self, db: Session):
        self.db = db
        self.auth_repository = AuthRepository(db)

    def execute(self, username: str, password: str, is_admin: bool = False):
        if self.auth_repository.user_exists(username):
            raise UserAlreadyExistsError("این نام کاربری قبلاً انتخاب شده است.")

        hashed_password = HashPassword().execute(password)

        return self.auth_repository.create_user(username, hashed_password, is_admin)
