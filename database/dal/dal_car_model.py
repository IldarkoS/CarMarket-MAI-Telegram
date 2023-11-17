from sqlalchemy.orm import Session
from database import CarModel

class CarModelDAL:
    def __init__(self, session: Session):
        self.session = session

    def get_all_models(self, CarModel, mark):
        return self.session.query(CarModel).filter(CarModel.id_mark == mark).all()

    def get_model_by_name(self, CarModel, name):
        return self.session.query(CarModel).filter(CarModel.name_model == name).first()
