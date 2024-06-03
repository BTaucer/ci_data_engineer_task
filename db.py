from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime

# change if needed (postgresql://username:password@host:port/database)
DATABASE_URL = 'postgresql://korisnik:1234@localhost/c_and_i'

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'

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


def connect_to_db():
    try:
        engine = create_engine(DATABASE_URL)
        session = sessionmaker(bind=engine)()
        return session
    except Exception as error:
        print("Error connecting to database:", error)
        return None


def insert_player(row):
    session = connect_to_db()
    if not session:
        return

    try:
        new_player = Player(
            player_id="None",
            url=row["url"],
            name=row["name"],
            full_name=row["full_name"],
            date_of_birth=row["date_of_birth"],
            age=row["age"],
            place_of_birth=row["place_of_birth"],
            country_of_birth=row["country_of_birth"],
            positions=row["positions"],
            current_club=row["current_club"],
            national_team=row["national_team"],
            appearances_current_club=row["appearances_current_club"],
            goals_current_club=row["goals_current_club"],
            scraping_timestamp=datetime.now().isoformat()
        )
        session.add(new_player)
        session.commit()

    except Exception as error:
        print("Error:", error)

    finally:
        session.close()
