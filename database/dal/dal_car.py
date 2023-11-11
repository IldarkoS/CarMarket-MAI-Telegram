from sqlalchemy.orm import Session


class CarDAL:
    def __init__(self, session: Session):
        self.session = session
