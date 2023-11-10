from sqlalchemy import Integer, SmallInteger
from sqlalchemy.orm import mapped_column
from database.models import Base


class CarGenerationPeriod(Base):
    __tablename__ = "car_generation_period"

    id_generation_period = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_year = mapped_column(SmallInteger, nullable=False)
    finish_year = mapped_column(SmallInteger, nullable=False)
