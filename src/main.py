import logging
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api import router
from src.core.db import db
from src.core.log_config import configure_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
	yield
	await db.close()

configure_logging(level=logging.DEBUG)

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
	uvicorn.run(
		"src.main:app",
		reload=True
	)