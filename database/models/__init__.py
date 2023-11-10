from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from database.models.car import Car
from database.models.car_condition import CarCondition
from database.models.car_generation import CarGeneration
from database.models.car_mark import CarMark
from database.models.car_type import CarType
from database.models.car_colour import CarColour
from database.models.car_engine import CarEngine
from database.models.car_gearbox import CarGearbox
from database.models.car_generation_period import CarGenerationPeriod
from database.models.car_performance_characteristic import CarPerformanceCharacteristic
from database.models.car_model import CarModel
from database.models.car_photo import CarPhoto
