from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import mapped_column
from database.models import Base


class CarPhoto(Base):
    __tablename__ = "car_photo"

    id_photo = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_car = mapped_column(ForeignKey('car.id_car'), nullable=False)
    dir_photo = mapped_column(String, nullable=False)
