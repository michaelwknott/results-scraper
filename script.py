from datetime import datetime
from typing import Any

import requests
from requests import JSONDecodeError, Response


def get_number_of_pages() -> int:
    """Gets the number of competition pages on the FINA API

    Returns:
        The number of pages, containing competition metadata, available on the
        FINA API.
    """
    url = "https://api.fina.org/fina/competitions?page=0&pageSize=100"
    response = session.get(url)
    decoded_response = decode_json_response(response)
    return decoded_response["pageInfo"]["numPages"]


def decode_json_response(response: Response) -> dict:
    """Decodes a response object, containing json data, to a python dict.

    Args:
        response: A requests response object fetched from the FINA API.

    Returns:
        A Python dictionary containing deserialised json data.
    """
    try:
        return response.json()
    except JSONDecodeError as exc:
        print(f"Response contains invalid JSON and could not be decoded\n {exc}")
        raise


def get_competitions_metadata(page_number: int) -> Response:
    """Gets the metadata for competitions on the given page of the FINA API.

    Args:
        page_number: A number representing a FINA API competitions metadata
        page.

    Returns:
        A requests Response object containing competitions metadata.
    """
    url = f"https://api.fina.org/fina/competitions?page={page_number}&pageSize=100"
    return requests.get(url)


def parse_competitions_metadata(comps_meta: dict) -> list[tuple[Any, ...]]:
    """Parses competitions metadata from the FINA API.

    Args:
        comps_meta: A dictionary containing competition metadata.

    Returns:
        A list of tuples containing parsed competition metadata including
        competition name and id.
    """
    comps_list: list[tuple[Any, ...]] = []
    competitions = comps_meta["content"]
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
    comp_dict: A dictionary containing an individual competition's
    metadata.

    Returns:
    The value associated with the dictionary key. If a KeyError
    is thrown, None is returned.
    """
    key1, key2 = args
    try:
        return comp_dict[key1][key2]
    except KeyError:
        return None


# Requests session hook functions
def check_for_errors(resp, *args, **kwargs):
    resp.raise_for_status()


if __name__ == "__main_":
    session = requests.Session()
    session.hooks["response"] = [check_for_errors]

    comps_data_list = []

    number_of_pages = get_number_of_pages()
    for page in range(number_of_pages + 1):
        comps_metadata_response = get_competitions_metadata(page)
        comps_metadata_dict = decode_json_response(comps_metadata_response)
        partial_comps_data_list = parse_competitions_metadata(comps_metadata_dict)
        comps_data_list.extend(partial_comps_data_list)
