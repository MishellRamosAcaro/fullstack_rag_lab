from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_database_settings, get_login_settings, get_rag_settings
from database import Base, get_engine
from models import User  # noqa: F401
from routers import auth
from routers import rag

app = FastAPI()


def build_settings() -> dict[str, object]:
    return {
        "rag": get_rag_settings(),
        "database": get_database_settings(),
        "login": get_login_settings(),
    }


app.state.settings = build_settings()

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
    Base.metadata.create_all(bind=get_engine())
