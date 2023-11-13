from sqlalchemy import Integer, ForeignKey, String, SmallInteger
from sqlalchemy.orm import mapped_column
from database.models import Base


class Car(Base):
    __tablename__ = "car"

    id_car = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_colour = mapped_column(ForeignKey('car_colour.id_colour'), nullable=False)
    id_condition = mapped_column(ForeignKey('car_condition.id_condition'), nullable=False)
    id_model = mapped_column(ForeignKey('car_model.id_model'), nullable=False)
    id_engine = mapped_column(ForeignKey('car_engine.id_engine'), nullable=False)
    id_gearbox = mapped_column(ForeignKey('car_gearbox.id_gearbox'), nullable=False)
    year = mapped_column(SmallInteger, nullable=False)
    mileage = mapped_column(Integer, nullable=False)
    price = mapped_column(Integer, nullable=False)
    owner_mobile = mapped_column(String, nullable=False)
