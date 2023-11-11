from sqlalchemy.orm import Session


class CarTypeDAL:
    def __init__(self, session: Session):
        self.session = session
