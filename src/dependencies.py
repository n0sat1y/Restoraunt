from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import db
from src.repositories import TableRepository
from src.services import TableService


SessionDep = Annotated[AsyncSession, Depends(db.session)]

def get_table_repository(session: SessionDep):
	return TableRepository(session=session)


def get_table_service(repo = Depends(get_table_repository)):
	return TableService(repo=repo)