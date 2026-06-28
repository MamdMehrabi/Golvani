from datetime import datetime

from sqlalchemy.orm import Session

from app.domains.posts.repository import PostRepository
from app.common.exceptions import EmptyContentError


class CreatePost:

    def __init__(self, db: Session):
        self.db = db
        self.post_repository = PostRepository(db)

    def execute(self, username: str, content: str):
        if not content or not content.strip():
            raise EmptyContentError("محتوای پست نمی‌تواند خالی باشد.")

        time = datetime.now().strftime("%H:%M")
        return self.post_repository.create_post(username, content, time)
