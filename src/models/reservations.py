from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

class ReservationModel(Base):
	__tablename__ = 'reservations'

	id: Mapped[int] = mapped_column(primary_key=True)
	customer_name: Mapped[str] = mapped_column(nullable=False)
	reservation_time: Mapped[datetime] = mapped_column(nullable=False)
	duration_minutes: Mapped[int] = mapped_column(nullable=False)
	table_id: Mapped[int] = mapped_column(ForeignKey('tables.id', ondelete='CASCADE'), nullable=False)

	table: Mapped["TableModel"] = relationship(back_populates="reservations")