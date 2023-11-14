from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from database.models import Base


class CarModel(Base):
    __tablename__ = "car_model"

    id_model = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_mark = mapped_column(ForeignKey('car_mark.id_mark'), nullable=False)
    name_model = mapped_column(String(20), nullable=False)

    mark: Mapped[List["CarMark"]] = relationship(back_populates="models")
    cars: Mapped[List["Car"]] = relationship(back_populates="model")
