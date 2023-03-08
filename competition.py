"""Fetch and store competition names and API ids from the FINA API.

The following endpoint is called to fetch the competition names
and ids:

"https://api.fina.org/fina/competitions?page=0&pageSize=100"

Each competition name and id will be used to fetch disipline names and
ids that took place at the competition.
"""

import csv
import pathlib
from datetime import datetime
from typing import Any

import requests
from requests import JSONDecodeError, Response

HEADERS = [
    "comp_id",
    "comp_name",
    "year",
    "month",
    "date_from",
    "date_to",
    "country_code",
    "city",
    "comp_type",
    "disciplines",
]


def get_number_of_pages(session: requests.Session) -> int:
    """Gets the number of pages of competition summary data on the FINA API.

    Returns:
        The number of pages, containing competition summary data, available
        on the FINA API.
    """
    url = "https://api.fina.org/fina/competitions?page=0&pageSize=100"
    response = session.get(url)
    decoded_response = decode_json_response(response)
    return decoded_response["pageInfo"]["numPages"]


def decode_json_response(response: Response) -> dict:
    """Decodes a response object, containing json data, to a python dict.

    Args:
        response: A requests Response object fetched from the FINA API.

    Returns:
        A Python dictionary containing deserialised json data.
    """
    try:
        return response.json()
    except JSONDecodeError as exc:
        print(f"Response contains invalid JSON and could not be decoded\n {exc}")
        raise


def get_competitions_summary_data(
    session: requests.Session, page_number: int
) -> Response:
    """Gets the summary data for competitions on the given page of the FINA API.

    Args:
        page_number: A number representing a FINA API competitions summary
        page.

    Returns:
        A requests Response object containing competitions summary data.
    """
    url = f"https://api.fina.org/fina/competitions?page={page_number}&pageSize=100"
    return session.get(url)


def parse_competitions_summary_data(comps_summary: dict) -> list[tuple[Any, ...]]:
    """Parses competitions summary data from the FINA API.

    Args:
        comps_summary: A dictionary containing competition summary data.

    Returns:
        A list of tuples containing parsed competition summary data.
    """
    comps_list: list[tuple[Any, ...]] = []
    competitions = comps_summary["content"]
    for competition in competitions:
        comp_id = competition["id"]
        name = competition["name"]
        date_from = competition["dateFrom"]
        date_to = competition["dateTo"]
        year = datetime.strptime(date_from, "%Y-%m-%dT%H:%M:%SZ").year
        month = datetime.strptime(date_from, "%Y-%m-%dT%H:%M:%SZ").month
        country_code = index_nested_dict_key(competition, "location", "countryCode")
        city = index_nested_dict_key(competition, "location", "city")
        comp_type = index_nested_dict_key(competition, "competitionType", "name")
        disciplines = " ".join(competition["disciplines"])

        row = (
            comp_id,
            name,
            year,
            month,
            date_from,
            date_to,
            country_code,
            city,
            comp_type,
            disciplines,
        )
        comps_list.append(row)
    return comps_list


def index_nested_dict_key(comp_dict: dict, *args: str) -> str | int | None:
    """Catches KeyError when indexing nested dictionary keys.

    Args:
    comp_dict: A dictionary containing an individual competition's summary
    data.
    args: Nested dictionary keys for the required value.

    Returns:
    The value associated with the dictionary key. If a KeyError
    is thrown, None is returned.
    """
    key1, key2 = args
    try:
        return comp_dict[key1][key2]
    except KeyError:
        return None


def create_csv(data_list: list[tuple], header: list[str]) -> None:
    """Takes a list of tuples and converts each tuple to a row in a csv file.

    Args:
        data_list: A list of dictionaries containing competition API id, name,
        year, start date, end date, country code, city, type and disciplines.
        header: A list of strings used as the header row when creating the
        csv file.
    """
    filepath = pathlib.Path.cwd() / "data/fina_all_competition_ids.csv"
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for item in data_list:
            writer.writerow(item)


# Requests session hook functions
def check_for_errors(resp, *args, **kwargs):
    resp.raise_for_status()


def main() -> None:
    session = requests.Session()
    session.hooks["response"] = [check_for_errors]

    comps_data_list = []

    number_of_pages = get_number_of_pages(session)
    for page in range(number_of_pages + 1):
        comps_summary_data_response = get_competitions_summary_data(session, page)
        comps_summary_data_dict = decode_json_response(comps_summary_data_response)
        partial_comps_data_list = parse_competitions_summary_data(
            comps_summary_data_dict
        )
        comps_data_list.extend(partial_comps_data_list)

    create_csv(comps_data_list, HEADERS)


if __name__ == "__main__":
    main()
