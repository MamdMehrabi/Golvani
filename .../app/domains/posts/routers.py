from datetime import datetime

from fastapi import APIRouter, Depends, Form, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.domains.posts.models import Post
from app.database import get_db
from app.core.templates import templates

router = APIRouter()

@router.get("/home", response_class=HTMLResponse)
def home_page(request: Request, username: str, db: Session = Depends(get_db)):
    get_post = db.query(Post)
    return templates.TemplateResponse(request, "chat.html", {
        "page": "home", 
        "username": username,
        "posts": get_post
    })

@router.post("/post/create")
def create_post(username: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    if content.strip():
        new_post = Post(username=username, content=content, time=datetime.now().strftime("%H:%M"))
        db.add(new_post)
        db.commit()
    return RedirectResponse(url=f"/home?username={username}", status_code=status.HTTP_303_SEE_OTHER)
