from sqlalchemy.orm import Session


class CarEngineDAL:
    def __init__(self, session: Session):
        self.session = session
