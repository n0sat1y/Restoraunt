from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

class TableModel(Base):
	__tablename__ = 'tables'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(unique=True, nullable=False)
	seats: Mapped[int] = mapped_column(nullable=False)
	location: Mapped[str] = mapped_column(nullable=False)

	reservations: Mapped[list["ReservationModel"]] = relationship(back_populates="table", cascade='all, delete', passive_deletes=True)