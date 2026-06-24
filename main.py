from fastapi import FastAPI, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session
from fastapi.websockets import WebSocket, WebSocketDisconnect
import bcrypt

from datetime import datetime
import models
from database import engine, get_db, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_user(username: str, password: str, is_admin : False):
    db = SessionLocal()
    hashed_pwd = hash_password(password)
    new_user = models.User(username=username, hashed_password=hashed_pwd, is_admin=is_admin)
    db.add(new_user)
    db.commit()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"page": "login"})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        return templates.TemplateResponse(request, "chat.html", {
            "page": "login", 
            "error": "نام کاربری یا رمز عبور اشتباه است."
        })
    return RedirectResponse(url=f"/home?username={username}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"page": "register"})

@app.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    create_user(username=username, password=password, is_admin=False)
    if db_user:
        return templates.TemplateResponse(request, "chat.html", {
            "page": "register", 
            "error": "این نام کاربری قبلاً انتخاب شده است."
        })
    return RedirectResponse(url=f"/home?username={username}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request, username: str, db: Session = Depends(get_db)):
    get_post = db.query(models.Posts)
    return templates.TemplateResponse(request, "chat.html", {
        "page": "home", 
        "username": username,
        "posts": get_post
    })

@app.post("/post/create")
def create_post(username: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    if content.strip():
        new_post = models.Posts(username=username, content=content, time=datetime.now().strftime("%H:%M"))
        db.add(new_post)
        db.commit()
    return RedirectResponse(url=f"/home?username={username}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request, username: str):
    return templates.TemplateResponse(request, "chat.html", {"page": "chat", "username": username})

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast(f"📢 {username} وارد چت روم شد")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"👤 {username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"❌ {username} چت روم را ترک کرد")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)