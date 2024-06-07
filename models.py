from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    player_id = Column(String, nullable=True)
    url = Column(String)
    name = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    age = Column(String, nullable=True)
    place_of_birth = Column(String, nullable=True)
    country_of_birth = Column(String, nullable=True)
    positions = Column(String, nullable=True)
    current_club = Column(String, nullable=True)
    national_team = Column(String, nullable=True)
    appearances_current_club = Column(Integer, nullable=True)
    goals_current_club = Column(Integer, nullable=True)
    scraping_timestamp = Column(DateTime)
