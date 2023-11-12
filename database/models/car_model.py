from sqlalchemy import Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import mapped_column
from database.models import Base


class CarModel(Base):
    __tablename__ = "car_model"

    id_model = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_mark = mapped_column(ForeignKey('car_mark.id_mark'), nullable=False)
    name_model = mapped_column(String(20), nullable=False)
