from sqlalchemy.orm import Session
from database import CarGearbox

class CarGearboxDAL:
    def __init__(self, session: Session):
        self.session = session

    def get_all_gearboxes(self, CarGearbox):
        return self.session.query(CarGearbox).filter(CarGearbox.id_gearbox is not None).all()

    def get_gearbox_by_type(self, CarGearbox, name):
        if name is None:
            return self.session.query(CarGearbox).filter(CarGearbox.gear_type == 'Автомат').first()
        return self.session.query(CarGearbox).filter(CarGearbox.gear_type == name).first()
