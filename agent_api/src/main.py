from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.api import chat

async def lifespan(app: FastAPI):
    # Perform any startup tasks here
    yield
    # Perform any shutdown tasks here

app = FastAPI(
    title = "Article Agent API",
    description = "API for the Article Agent application.",
    version = "1.0.0",
    lifespan = lifespan
)

app.include_router(chat.router,prefix="/api/chat",tags = ["chat"])