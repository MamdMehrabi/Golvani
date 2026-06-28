from sqlalchemy.orm import Session

from app.domains.posts.repository import PostRepository


class GetPosts:

    def __init__(self, db: Session):
        self.db = db
        self.post_repository = PostRepository(db)

    def execute(self):
        return self.post_repository.get_all_posts()
