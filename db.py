from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select

from datetime import datetime
from models import Player

# change if needed (postgresql://username:password@host:port/database)
DATABASE_URL = 'postgresql://korisnik:1234@localhost/c_and_i'


def connect_to_db():
    try:
        engine = create_engine(DATABASE_URL)
        session = sessionmaker(bind=engine)()
        return session

    except Exception as error:
        print("Error connecting to database:", error)
        return None


def insert_player(row: dict):
    session = connect_to_db()
    if not session:
        return

    try:
        new_player = Player(
            player_id=row["player_id"],
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
            scraping_timestamp=row["scraping_timestamp"]
        )
        session.add(new_player)
        session.commit()

    except Exception as error:
        print("Error:", error)

    finally:
        session.close()


def select_player(url: str):
    try:
        session = connect_to_db()
        query = select(Player)
        players = session.execute(query).fetchall()
        urls = set([player[0].url for player in players])
        print(url in urls)
    except Exception as error:
        print("Error:", error)

    finally:
        session.close()


def update_player(row: dict):
    try:
        session = connect_to_db()
        query = select(Player).where(Player.url == row["url"])
        player = session.execute(query).fetchall()

        print(player[0][0].current_club)
    except Exception as error:
        print("Error:", error)

    finally:
        session.close()


def player_in_database(url: str) -> bool:
    try:
        session = connect_to_db()
        query = select(Player.url)
        urls = session.execute(query).fetchall()
        urls = set([url[0] for url in urls])
        return url in urls

    except Exception as error:
        print("Error:", error)

    finally:
        session.close()


update_player({"url": "https://en.wikipedia.org/wiki/Mario_Perrone"})
# select_player("https://en.wikipedia.org/wiki/Mario_Perrone")
