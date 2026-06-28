from fastapi import FastAPI

from app.database import create_tables
from app.domains import router

create_tables()

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
