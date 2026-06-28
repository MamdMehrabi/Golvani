from fastapi import APIRouter, Depends, Form, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.templates import templates
from app.database import get_db
from app.domains.auth.models import User
from app.domains.auth.usecases.hash_password import HashPassword
from app.domains.auth.usecases.verify_password import VerifyPassword

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"page": "login"})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or not VerifyPassword().execute(password, db_user.hashed_password):
        return templates.TemplateResponse(request, "chat.html", {
            "page": "login", 
            "error": "نام کاربری یا رمز عبور اشتباه است."
        })
    return RedirectResponse(url=f"/home?username={username}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"page": "register"})

@router.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        return templates.TemplateResponse(request, "chat.html", {
            "page": "register", 
            "error": "این نام کاربری قبلاً انتخاب شده است."
        })
    
    hashed_pwd = HashPassword().execute(password)
    new_user = User(username=username, hashed_password=hashed_pwd, is_admin=False)
    db.add(new_user)
    db.commit()
    
    return RedirectResponse(url=f"/home?username={username}", status_code=status.HTTP_303_SEE_OTHER)
