from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket

from app.domains.chat.usecases.connection_manager import manager
from app.core.templates import templates

router = APIRouter()

@router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request, username: str):
    return templates.TemplateResponse(request, "chat.html", {"page": "chat", "username": username})

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast(f"📢 {username} وارد چت روم شد")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"👤 {username}: {data}")
    except:
        manager.disconnect(websocket)
        await manager.broadcast(f"❌ {username} چت روم را ترک کرد")
