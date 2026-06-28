from sqlalchemy.orm import Session

from app.domains.posts.models import Post


class PostRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_posts(self) -> list[Post]:
        return self.db.query(Post).all()  # type: ignore

    def create_post(self, username: str, content: str, time: str) -> Posts:
        post = Post(
            username=username,
            content=content,
            time=time
        )
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
