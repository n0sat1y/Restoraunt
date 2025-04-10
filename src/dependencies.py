from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import db

SessionDep = Annotated[AsyncSession, Depends(db.session)]