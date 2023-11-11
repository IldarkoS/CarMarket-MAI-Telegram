from sqlalchemy.orm import Session


class CarMarkDAL:
    def __init__(self, session: Session):
        self.session = session
