"""Scrapes and parse discipline results for individual swimming
competitions from the FINA API.

The following endpoint is called to scrape disipline names and ids for
indivudal competitions:

"https://api.fina.org/fina/competitions/{comp_id}/events"

*{comp_id} should be replaced with the required competition id.

The following endpoint is called to scrape individual disipline results for
competitions:

"https://api.fina.org/fina/events/{discipline_id}"

*{discipline_id} should be replaced with the requried discipline id.
"""

import requests
from requests import Response

from competition import decode_json_response


def get_individual_competition_summary_data(comp_id: int) -> Response:
    """Gets data related to the competition from the FINA API.

    Args:
        comp_id: API parameter that identifies the competition.

    Returns:
        A Response object containing summary data related to the sports and
        disciplines included at the competition.
    """
    url = f"https://api.fina.org/fina/competitions/{comp_id}/events"
    return requests.get(url)


def parse_discipline_names_and_ids(comp_summary: dict) -> dict[str, str]:
    """Parses discipline name and id from competition summary data.

    Args:
        comp_meta: Summary data related to the sports and disciplines included
        at the competition.

    Returns:
        A dictionary containing discipline name and discispline id as
        key: value pairs.
    """

    discipline_names_ids = {}
    discipline_list = comp_summary["Sports"][1]["DisciplineList"]
    for item in discipline_list:
        discipline = item["DisciplineName"]
        discipline_id = item["Id"]
        discipline_names_ids[discipline] = discipline_id
    return discipline_names_ids


def get_discipline_data(discipline_id: str) -> Response:
    """Gets json results data for the requested discipline from the FINA API.

    Args:
        discipline_id: API parameter that identifies the discipline

    Returns:
        A Response object containing results data for the discipline.
    """
    url = f"https://api.fina.org/fina/events/{discipline_id}"
    return requests.get(url)


if __name__ == "__main__":
    comp_response = get_individual_competition_summary_data(5)
    comp_data = decode_json_response(comp_response)
    discipline_names_ids = parse_discipline_names_and_ids(comp_data)
    print(discipline_names_ids)
    discipline_id = discipline_names_ids["Women 50m Freestyle"]
    women_50m_freestyle_response = get_discipline_data(discipline_id)
    women_50m_freestyle_data = decode_json_response(women_50m_freestyle_response)

    print(women_50m_freestyle_data)
