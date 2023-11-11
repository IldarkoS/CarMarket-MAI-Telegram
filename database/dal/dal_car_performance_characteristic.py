from sqlalchemy.orm import Session


class CarPerformanceCharacteristicDAL:
    def __init__(self, session: Session):
        self.session = session
