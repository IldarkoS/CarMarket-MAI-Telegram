from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped
from database.models import Base


class CarCondition(Base):
    __tablename__ = "car_condition"

    id_condition = mapped_column(Integer, primary_key=True, autoincrement=True)
    _condition = mapped_column(String(20), nullable=False)

    cars: Mapped[List["Car"]] = relationship(back_populates="condition")
