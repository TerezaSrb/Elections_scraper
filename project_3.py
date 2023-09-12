"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Tereza Srbová
email: terezasrbova.ts@gmail.com
discord: Tereza S#9721
"""
import csv
import requests
import sys

from bs4 import BeautifulSoup


MAIN_URL = "https://www.volby.cz/pls/ps2017nss/"

HEADER = ["code", "location", "registered", "envelopes", "valid"]

HEADER_COMPLETE = False

DATA = []


def get_tables(url):
    server_response = requests.get(url)
    soup = BeautifulSoup(server_response.text, 'html.parser')
    return soup.find_all("table", {"class": "table"})


def select_area(url, area):
    tables = get_tables(url)
    for table in tables:
        table_rows = table.find_all("tr")
        for table_row in table_rows:
            table_datas = table_row.find_all("td")
            if len(table_datas) >= 4 and area == table_datas[1].text:
                return table_datas[3].find("a").get('href')
    return None


def browse_all_municipalities(url):
    tables = get_tables(url)

    codes = []
    locations = []
    links = []

    for table in tables:
        table_rows = table.find_all("tr")
        for table_row in table_rows:
            table_datas = table_row.find_all("td")
            if len(table_datas) >= 3 and table_datas[2].text == "X":
                codes.append(table_datas[0].text)
                locations.append(table_datas[1].text)
                links.append(table_datas[2].find("a").get('href'))
    return codes, locations, links


def get_precinct_links(table):
    precinct_links = []
    table_datas = table.find_all("td")
    table_datas = [table_data for table_data in table_datas if (
            table_data.find("a") is not None)]
    for table_data in table_datas:
        precinct_link = table_data.find("a").get('href')
        precinct_links.append(precinct_link)
    return precinct_links


def get_data_for_municipality(code, location, link):
    registered = 0
    envelopes = 0
    valid = 0
    votes = []

    tables = get_tables(MAIN_URL + link)
    print(f"Vyčítání dat pro obec {location}.")

    if len(tables) == 1:  # Obec má více okrsků
        precinct_links = get_precinct_links(tables[0])
        for link in precinct_links:
            precinct_tables = get_tables(MAIN_URL + link)
            (registered_in_precinct, envelopes_in_precinct,
             valid_in_precinct) = get_votes_overview_for_precinct(
                precinct_tables[0])
            registered += registered_in_precinct
            envelopes += envelopes_in_precinct
            valid += valid_in_precinct
            votes = add_list_items(
                votes, get_votes_for_parties(precinct_tables[1:]))

    else:  # Obec má jen jeden okrsek
        registered, envelopes, valid = get_votes_overview(
            tables[0])
        if not HEADER_COMPLETE:
            create_header(tables[1:])
        votes = get_votes_for_parties(tables[1:])

    DATA.append([code, location, registered, envelopes, valid] + votes)


def get_votes_overview(table):
    table_rows = table.find_all("tr")
    table_datas = table_rows[2].find_all("td")
    registered = int("".join(table_datas[3].text.split()))
    envelopes = int("".join(table_datas[4].text.split()))
    valid = int("".join(table_datas[7].text.split()))
    return registered, envelopes, valid


def get_votes_overview_for_precinct(table):
    table_rows = table.find_all("tr")
    table_datas = table_rows[1].find_all("td")
    registered = int("".join(table_datas[0].text.split()))
    envelopes = int("".join(table_datas[1].text.split()))
    valid = int("".join(table_datas[4].text.split()))
    return registered, envelopes, valid


def create_header(tables):
    global HEADER_COMPLETE
    for table in tables:
        table_rows = table.find_all("tr")
        for table_row in table_rows:
            table_datas = table_row.find_all("td")
            if len(table_datas) == 5 and table_datas[0].text != "-":
                HEADER.append(table_datas[1].text)
    HEADER_COMPLETE = True


def get_votes_for_parties(tables):
    votes = []
    for table in tables:
        table_rows = table.find_all("tr")
        for table_row in table_rows:
            table_datas = table_row.find_all("td")
            if len(table_datas) == 5 and table_datas[0].text != "-":
                votes.append(table_datas[2].text)
    return votes


def add_list_items(list1, list2):
    new_list = []
    if not list1:
        return list2
    if not list2:
        return list1
    if len(list1) != len(list2):
        print("Listy nelze sčítat, nemají stejnou délku.")
    for i in range(len(list1)):
        value1 = int(list1[i]) if type(list1[i]) == int else int(
            "".join(list1[i].split()))
        value2 = int(list2[i]) if type(list2[i]) == int else int(
            "".join(list2[i].split()))
        new_list.append(value1 + value2)
    return new_list


def save_in_csv(filename):
    with open(filename, 'w', newline="") as f:
        write = csv.writer(f, delimiter=';')
        write.writerow(HEADER)
        write.writerows(DATA)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Soubor: {sys.argv[0]} potřebuje dva povinné argumenty!")
    elif not sys.argv[2].endswith(".csv"):
        print(f"Cílový soubor: {sys.argv[2]} není ve formátu .csv!")

    area_link = select_area(MAIN_URL + "ps3?xjazyk=CZ", sys.argv[1])
    if area_link is None:
        print("Neplatný název územního celku!")
    else:
        municipality_codes, municipality_locations, municipality_links = \
            browse_all_municipalities(MAIN_URL + area_link)
        for location_index in range(len(municipality_codes)):
            get_data_for_municipality(municipality_codes[location_index],
                                      municipality_locations[location_index],
                                      municipality_links[location_index])
        save_in_csv(sys.argv[2])
