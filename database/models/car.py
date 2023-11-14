from sqlalchemy import Integer, ForeignKey, String, SmallInteger
from sqlalchemy.orm import mapped_column, relationship, Mapped
from database.models.car_colour import CarColour
from database.models.car_condition import CarCondition
from database.models.car_model import CarModel
from database.models.car_engine import CarEngine
from database.models.car_gearbox import CarGearbox
from database.models.car_mark import CarMark
from database.models import Base

from database.session import Session
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
    dir_photo = mapped_column(String, nullable=False)

    colour: Mapped["CarColour"] = relationship(back_populates="cars")
    condition: Mapped["CarCondition"] = relationship(back_populates="cars")
    model: Mapped["CarModel"] = relationship(back_populates="cars")
    engine: Mapped["CarEngine"] = relationship(back_populates="cars")
    gearbox: Mapped["CarGearbox"] = relationship(back_populates="cars")
