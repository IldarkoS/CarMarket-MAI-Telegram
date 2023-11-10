from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
from database.models import Base


class CarColour(Base):
    __tablename__ = "car_colour"

    id_colour = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_colour = mapped_column(String(20), nullable=False)
