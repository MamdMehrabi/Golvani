from sqlalchemy.orm import Session

from app.domains.auth.repository import AuthRepository
from app.domains.auth.usecases.verify_password import VerifyPassword
from app.common.exceptions import InvalidCredentialsError


class LoginUser:

    def __init__(self, db: Session):
        self.db = db
        self.auth_repository = AuthRepository(db)

    def execute(self, username: str, password: str):
        user = self.auth_repository.get_user_by_username(username)

        if not user:
            raise InvalidCredentialsError("نام کاربری یا رمز عبور اشتباه است.")

        if not VerifyPassword().execute(password, user.hashed_password):
            raise InvalidCredentialsError("نام کاربری یا رمز عبور اشتباه است.")

        return user