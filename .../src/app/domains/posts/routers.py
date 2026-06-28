from fastapi import APIRouter, Depends, Form, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.templates import templates
from app.database import get_db
from app.domains.posts.usecases import CreatePost, GetPosts
from app.common.exceptions import EmptyContentError

router = APIRouter()


@router.get("/home", response_class=HTMLResponse)
def home_page(request: Request, username: str, db: Session = Depends(get_db)):
    get_posts_usecase = GetPosts(db)
    posts = get_posts_usecase.execute()

    return templates.TemplateResponse(request, "chat.html", {
        "page": "home",
        "username": username,
        "posts": posts
    })


@router.post("/post/create")
def create_post(
        username: str = Form(...),
        content: str = Form(...),
        db: Session = Depends(get_db)
):
    try:
        create_post_usecase = CreatePost(db)
        create_post_usecase.execute(username, content)

    except EmptyContentError:
        pass

    return RedirectResponse(url=f"/home?username={username}", status_code=status.HTTP_303_SEE_OTHER)
