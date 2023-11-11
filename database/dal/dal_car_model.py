from sqlalchemy.orm import Session


class CarModelDAL:
    def __init__(self, session: Session):
        self.session = session
