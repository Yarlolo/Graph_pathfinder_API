from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine, Base_class
from app.api.endpoints import auth, graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Начало...")
    Base_class.metadata.create_all(bind=engine)
    yield
    print("Выключение...")

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api", tags=["Пользовател"])
app.include_router(graph.router, prefix="/api", tags=["Граф"])
