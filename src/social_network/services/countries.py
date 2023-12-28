from fastapi import Depends

from src.social_network.db import tables
from src.social_network.db.session import Session, get_session


class CountriesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_countries(self) -> list[tables.Country]:
        return self.session.query(tables.Country).all()
