from sqlalchemy import Integer, ForeignKey, String, SmallInteger
from sqlalchemy.orm import mapped_column
from database.models import Base


class Car(Base):
    __tablename__ = "car"

    id_car = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_performance_characteristic = mapped_column(ForeignKey(
        'car_performance_characteristic.id_performance_characteristic'), nullable=False)
    id_colour = mapped_column(ForeignKey('car_colour.id_colour'), nullable=False)
    id_condition = mapped_column(ForeignKey('car_condition.id_condition'), nullable=False)
    year = mapped_column(SmallInteger, nullable=False)
    mileage = mapped_column(Integer, nullable=False)
    price = mapped_column(Integer, nullable=False)
    owner_mobile = mapped_column(String, nullable=False)
