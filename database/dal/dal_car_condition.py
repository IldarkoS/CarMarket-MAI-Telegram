from sqlalchemy.orm import Session


class CarConditionDAL:
    def __init__(self, session: Session):
        self.session = session
