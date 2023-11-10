from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from database.models import Base


class CarType(Base):
    __tablename__ = "car_type"

    id_type = mapped_column(Integer, primary_key=True, autoincrement=True)
    type_name = mapped_column(String(20), nullable=False)
