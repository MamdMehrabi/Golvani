from fastapi import APIRouter

from app.domains.auth import routers as auth_routers
from app.domains.chat import routers as chat_routers
from app.domains.posts import routers as posts_routers

router = APIRouter()

# Include routers
router.include_router(auth_routers.router)
router.include_router(posts_routers.router)
router.include_router(chat_routers.router)
