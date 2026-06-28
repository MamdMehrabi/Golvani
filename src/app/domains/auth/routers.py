from fastapi import APIRouter, Depends, Form, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.templates import templates
from app.database import get_db
from app.domains.auth.usecases import RegisterUser, LoginUser
from app.common.exceptions import UserAlreadyExistsError, InvalidCredentialsError

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"page": "login"})


@router.post("/login")
def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    try:
        login_usecase = LoginUser(db)
        user = login_usecase.execute(username, password)
        return RedirectResponse(url=f"/home?username={username}", status_code=status.HTTP_303_SEE_OTHER)

    except InvalidCredentialsError as e:
        return templates.TemplateResponse(request, "chat.html", {
            "page": "login",
            "error": str(e)
        })


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"page": "register"})


@router.post("/register")
def register(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    try:
        register_usecase = RegisterUser(db)
        user = register_usecase.execute(username, password, is_admin=False)
        return RedirectResponse(url=f"/home?username={username}", status_code=status.HTTP_303_SEE_OTHER)

    except UserAlreadyExistsError as e:
        return templates.TemplateResponse(request, "chat.html", {
            "page": "register",
            "error": str(e)
        })
