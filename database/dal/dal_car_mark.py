from sqlalchemy.orm import Session
from database import CarMark

class CarMarkDAL:
    def __init__(self, session: Session):
        self.session = session

    def get_all_marks(self, CarMark):
        return self.session.query(CarMark).filter(CarMark.id_mark is not None).all()

    def get_mark_by_name(self, CarMark, name):
        return self.session.query(CarMark).filter(CarMark.name_mark == name).first()

    def get_mark_by_id(self, CarMark, id_mark):
        return self.session.query(CarMark).filter(CarMark.id_mark == id_mark).first()
