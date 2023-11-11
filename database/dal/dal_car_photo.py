from sqlalchemy.orm import Session


class CarPhotoDAL:
    def __init__(self, session: Session):
        self.session = session
