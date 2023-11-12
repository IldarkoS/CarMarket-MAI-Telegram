from sqlalchemy import String, Integer, SmallInteger
from sqlalchemy.orm import mapped_column
from database.models import Base


class CarGearbox(Base):
    __tablename__ = "car_gearbox"

    id_gearbox = mapped_column(Integer, primary_key=True, autoincrement=True)
    gear_type = mapped_column(String(20), nullable=False)
