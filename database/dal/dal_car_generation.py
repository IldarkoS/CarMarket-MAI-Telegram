from sqlalchemy.orm import Session


class CarGenerationDAL:
    def __init__(self, session: Session):
        self.session = session
