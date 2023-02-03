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


# Requests session hook functions
def check_for_errors(resp, *args, **kwargs):
    resp.raise_for_status()


if __name__ == "__main_":
    session = requests.Session()
    session.hooks["response"] = [check_for_errors]

    number_of_pages = get_number_of_pages()
    for page in range(number_of_pages + 1):
        comps_metadata_response = get_competitions_metadata(page)
        comps_metadata_dict = decode_json_response(comps_metadata_response)
