from sqlalchemy.orm import Session
from database import Car, CarColour, CarCondition, CarMark, CarModel, CarEngine, CarGearbox


class CarDAL:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create(self, Model, **kwargs):
        if instance := self.session.query(Model).filter_by(**kwargs).first():
            return instance
        else:
            self.session.add(instance := Model(**kwargs))
            self.session.flush()
            return instance

    def create_car(self, name_mark: str, name_model: str, gear_type: str, fuel_type: str, condition: str,
                   hoursepower: int, caparcity: str, year: int, mileage: int, name_colour: str, price: int,
                   owner_mobile: str, dir_photo: str) -> Car:

        self.session.add(
            new_car := Car(model=self.get_or_create(Model=CarModel, name_model=name_model,
                                                    mark=self.get_or_create(Model=CarMark, name_mark=name_mark)),
                           gearbox=self.get_or_create(Model=CarGearbox, gear_type=gear_type),
                           engine=self.get_or_create(Model=CarEngine, fuel_type=fuel_type,
                                                     hoursepower=hoursepower, caparcity=caparcity),
                           condition=self.get_or_create(Model=CarCondition, _condition=condition),
                           colour=self.get_or_create(Model=CarColour, name_colour=name_colour),
                           mileage=mileage, year=year, price=price, owner_mobile=owner_mobile, dir_photo=dir_photo)
        )
        self.session.flush()
        return new_car

    def select_cars(self, Model, id_model, id_gearbox, min_mile, max_mile, min_price, max_price):
        return self.session.query(Model).\
            filter(Model.id_model == id_model).\
            filter(Model.id_gearbox == id_gearbox).\
            filter(Model.mileage >= min_mile). \
            filter(Model.mileage <= max_mile). \
            filter(Model.price <= max_price). \
            filter(Model.price >= min_price).all()

    def select_spec_car(self, Model, id_model, price, mileage):
        return self.session.query(Model).filter(Model.id_model == id_model).\
            filter(Model.price == price).filter(Model.mileage == mileage).first()