from contextlib import asynccontextmanager
from database import engine, Model
from fastapi import FastAPI
from router.books import router as books_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
		await conn.run_sync(Model.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(books_router)
