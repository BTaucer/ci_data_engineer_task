import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import requests

import datetime
import re
import sys

from db import insert_player, player_in_database, update_player


def read_data(html, tag, class_=None):
    content = html.find(tag, class_=class_)
    if content:
        content = content.text.replace("\n", "").replace("\xa0", "")
        content = str(re.sub(r'\[\d+\]', "", content))
    return content


def clean_nan(row: dict) -> dict:
    for key, value in row.items():
        if value is np.nan:
            row[key] = None
    return row


def convert_to_int(data: str) -> int | None:
    if not data:
        return None
    elif re.search(r'\d+', data):
        return int(re.search(r'\d+', data).group())
    else:
        return None


def get_data(url: str) -> dict:
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    main_table = soup.find("table", class_="infobox vcard")
    player_data = {}

    if not main_table:
        return

    # store data to dict
    player_data["url"] = url
    player_data["player_id"] = None
    player_data["scraping_timestamp"] = datetime.datetime.now().isoformat()
    player_data["name"] = read_data(main_table, "caption", class_="infobox-title fn")
    player_data["full_name"] = read_data(main_table, "td", class_="infobox-data nickname")
    player_data["date_of_birth"] = read_data(main_table, "span", class_="bday")

    player_data["age"] = convert_to_int(read_data(main_table, "span", class_="noprint ForceAgeToShow"))
    player_data["positions"] = read_data(main_table, "td", class_="infobox-data role")
    player_data["current_club"] = read_data(main_table, "td", class_="infobox-data org")

    birthplace = read_data(main_table, "td", class_="infobox-data birthplace")

    player_data["place_of_birth"] = None
    player_data["country_of_birth"] = None
    if birthplace:
        birthplace = list(birthplace.split(", "))
        player_data["place_of_birth"] = ", ".join(birthplace[0:-1])
        player_data["country_of_birth"] = birthplace[-1]

    player_data["appearances_current_club"] = None
    player_data["goals_current_club"] = None
    table_rows = list(main_table.findAll("tr"))
    for tr in table_rows:
        tr_data = read_data(tr, "td", class_="infobox-data infobox-data-a")
        if tr_data == player_data["current_club"]:
            player_data["appearances_current_club"] = convert_to_int(read_data(tr, "td", class_="infobox-data infobox-data-b"))
            player_data["goals_current_club"] = convert_to_int(read_data(tr, "td", class_="infobox-data infobox-data-c"))
            break

    player_data["national_team"] = read_data(main_table, "span", class_="country-name")

    return player_data


def scrap_links(filename: str):
    df_urls = pd.read_csv(filename)
    df_players = pd.DataFrame(columns=["url", "name", "full_name", "date_of_birth", "age", "place_of_birth", "country_of_birth", "positions", "current_club", "national_team", "appearances_current_club", "goals_current_club", "scraping_timestamp"])

    index = 0
    for url in df_urls["urls"]:
        player_data = get_data(url)
        if player_data:
            print(player_data)
            if player_in_database(player_data["url"]):
                update_player(player_data)
            else:
                insert_player(player_data)

            df_players.loc[index] = player_data
            index += 1
    df_players.to_csv("scrapped_data.csv")


def insert_initial_players(filename: str):
    df = pd.read_csv(filename, delimiter=";")
    for index, row in df.iterrows():
        row = dict(row)
        row["scraping_timestamp"] = datetime.datetime.now().isoformat()
        row["goals_current_club"] = None
        row["appearances_current_club"] = None
        row["age"] = convert_to_int(str(row["age"]))
        row = clean_nan(row)

        insert_player(row)


if __name__ == "__main__":
    insert_initial_players(sys.argv[1])

    update_players(sys.argv[2])
