from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column
from database.models import Base


class CarPerformanceCharacteristic(Base):
    __tablename__ = "car_performance_characteristic"

    id_performance_characteristic = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_generation = mapped_column(ForeignKey('car_generation.id_generation'), nullable=False)
    id_engine = mapped_column(ForeignKey('car_engine.id_engine'), nullable=False)
    id_gearbox = mapped_column(ForeignKey('car_gearbox.id_gearbox'), nullable=False)
    weight = mapped_column(Integer, nullable=False)
    start_price = mapped_column(Integer, nullable=False)
