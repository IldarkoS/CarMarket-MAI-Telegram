from sqlalchemy.orm import Session


class CarMarkDAL:
    def __init__(self, session: Session):
        self.session = session

    def get_all_marks(self, Model):
        return self.session.query(Model).filter(Model.id_mark is not None).all()

    def get_mark_by_name(self, Model, name):
        return self.session.query(Model).filter(Model.name_mark == name).first()

    def get_mark_by_id(self, Model, id_mark):
        return self.session.query(Model).filter(Model.id_mark == id_mark).first()
