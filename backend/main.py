from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from database import Base, engine
from models import User  # noqa: F401
from routers import auth
from routers import rag

app = FastAPI(title="Fullstack RAG COM")

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(rag.router)
app.include_router(auth.router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
