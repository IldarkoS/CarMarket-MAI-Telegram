from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column
from database.models import Base


class CarPerformanceCharacteristic(Base):
    __tablename__ = "car_performance_characteristic"

    id_performance_characteristic = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_model = mapped_column(ForeignKey('car_model.id_model'), nullable=False)
    id_engine = mapped_column(ForeignKey('car_engine.id_engine'), nullable=False)
    id_gearbox = mapped_column(ForeignKey('car_gearbox.id_gearbox'), nullable=False)
    weight = mapped_column(Integer, nullable=False)
