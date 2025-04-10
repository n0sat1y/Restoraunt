import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api import router
from src.core.db import db

@asynccontextmanager
async def lifespan(app: FastAPI):
	yield
	await db.close()

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
	uvicorn.run(
		"src.main:app",
		reload=True
	)