from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.api import chat
from src.db.session import init_engine, close_engine

async def lifespan(app: FastAPI):
    init_engine()
    yield
    close_engine()

app = FastAPI(
    title = "Article Agent API",
    description = "API for the Article Agent application.",
    version = "1.0.0",
    lifespan = lifespan
)

app.include_router(chat.router,prefix="/api/chat",tags = ["chat"])