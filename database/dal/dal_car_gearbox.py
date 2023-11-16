from sqlalchemy.orm import Session


class CarGearboxDAL:
    def __init__(self, session: Session):
        self.session = session

    def get_all_gearboxes(self, Model):
        return self.session.query(Model).filter(Model.id_gearbox is not None).all()

    def get_gearbox_by_type(self, Model, name):
        if name is None:
            return self.session.query(Model).filter(Model.gear_type == 'Автомат').first()
        return self.session.query(Model).filter(Model.gear_type == name).first()
