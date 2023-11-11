from sqlalchemy.orm import Session


class CarGenerationPeriodDAL:
    def __init__(self, session: Session):
        self.session = session
