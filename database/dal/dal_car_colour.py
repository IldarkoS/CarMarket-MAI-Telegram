from sqlalchemy.orm import Session


class CarColourDAL:
    def __init__(self, session: Session):
        self.session = session
