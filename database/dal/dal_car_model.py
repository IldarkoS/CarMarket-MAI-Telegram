from sqlalchemy.orm import Session


class CarModelDAL:
    def __init__(self, session: Session):
        self.session = session

    def get_all_models(self, Model, mark):
        return self.session.query(Model).filter(Model.id_mark == mark).all()

    def get_model_by_name(self, Model, name):
        return self.session.query(Model).filter(Model.name_model == name).first()
