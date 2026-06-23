from fastapi import FastAPI, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session
import user as models
from database import engine, get_db
from fastapi.websockets import WebSocket, WebSocketDisconnect
import bcrypt

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
    
    return RedirectResponse(url=f"/chat?username={username}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"page": "register"})


@app.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    
    
    if db_user:
        return templates.TemplateResponse(request, "chat.html", {
            "page": "register", 
            "error": "این نام کاربری قبلاً انتخاب شده است."
        })
    
    
    hashed_pwd = hash_password(password)
    new_user = models.User(username=username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    
    return RedirectResponse(url=f"/chat?username={username}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request, username: str):
    return templates.TemplateResponse(request, "chat.html", {"page": "chat", "username": username})

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast(f"📢 {username} وارد چت شد!")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"👤 {username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"❌ {username} چت را ترک کرد.")