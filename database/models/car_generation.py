from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column
from database.models import Base


class CarGeneration(Base):
    __tablename__ = "car_generation"

    id_generation = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_generation_period = mapped_column(ForeignKey('car_generation_period.id_generation_period'), nullable=False)
    id_type = mapped_column(ForeignKey('car_type.id_type'), nullable=False)
    id_model = mapped_column(ForeignKey('car_model.id_model'), nullable=False)
