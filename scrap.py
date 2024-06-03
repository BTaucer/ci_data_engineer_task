from bs4 import BeautifulSoup
import pandas as pd
import requests

import datetime
import re
import sys

from db import insert_player


def read_data(html, tag, class_=None):
    content = html.find(tag, class_=class_)
    if content:
        content = content.text.replace("\n", "").replace("\xa0", "")
        content = str(re.sub(r'\[\d+\]', "", content))
    return content


def convert_to_int(data: str) -> int | None:
    if not data:
        return None
    else:
        return int(re.search(r'\d+', data).group())


def get_data(url: str) -> dict:
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    main_table = soup.find("table", class_="infobox vcard")
    player_data = {}
    scraping_timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")

    if not main_table:
        return

    try:
        # store data to dict
        player_data["url"] = url
        player_data["scraping_timestamp"] = scraping_timestamp
        player_data["name"] = read_data(main_table, "caption", class_="infobox-title fn")
        player_data["full_name"] = read_data(main_table, "td", class_="infobox-data nickname")
        player_data["date_of_birth"] = read_data(main_table, "span", class_="bday")

        player_data["age"] = convert_to_int(read_data(main_table, "span", class_="noprint ForceAgeToShow"))
        player_data["positions"] = read_data(main_table, "td", class_="infobox-data role")
        player_data["current_club"] = read_data(main_table, "td", class_="infobox-data org")

        birthplace = read_data(main_table, "td", class_="infobox-data birthplace")
        if birthplace:
            birthplace = list(birthplace.split(", "))
            player_data["place_of_birth"] = ", ".join(birthplace[0:-1])
            player_data["country_of_birth"] = birthplace[-1]

        table_rows = list(main_table.findAll("tr"))
        for tr in table_rows:
            tr_data = read_data(tr, "td", class_="infobox-data infobox-data-a")
            if tr_data == player_data["current_club"]:
                player_data["appearances_current_club"] = convert_to_int(read_data(tr, "td", class_="infobox-data infobox-data-b"))
                player_data["goals_current_club"] = convert_to_int(read_data(tr, "td", class_="infobox-data infobox-data-c"))
                break

        player_data["national_team"] = read_data(main_table, "span", class_="country-name")

    except:
        pass

    return player_data


def main(filename: str):
    df_urls = pd.read_csv(filename)
    df_players = pd.DataFrame(columns=["url", "name", "full_name", "date_of_birth", "age", "place_of_birth", "country_of_birth", "positions", "current_club", "national_team", "appearances_current_club", "goals_current_club", "scraping_timestamp"])

    index = 0
    for url in df_urls["urls"]:
        player_data = get_data(url)
        if player_data:
            print(player_data)
            insert_player(player_data)
            df_players.loc[index] = player_data
            index += 1

    df_players.to_csv("scrapped_data.csv")


if __name__ == "__main__":
    main(sys.argv[1])
