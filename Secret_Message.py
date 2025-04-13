from typing import Optional

import numpy as np
import requests
from bs4 import BeautifulSoup


def download_html(url: str) -> Optional[str]:
    """
    Downloads content from published Google Doc URL.
    :param url: Google doc url(pub)
    :return: HTML content of the doc or None if not found
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading document or Invalid URL: {e}")
    raise ValueError ("Error downloading document or Invalid URL")



def fetch_xy_data_from_doc(html_content: str) -> Optional[dict]:
    """
    Parse the html content of the doc and return a dictionary with keys as coordinates and values as symbols
    :param html_content:
    :return: dictionary with x and y coordinates as keys and values as symbols
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        expected_headers = {"x-coordinate", "Character", "y-coordinate"}
        data = []
        x_axis = []
        y_axis = []
        unicode_char = []

        for table in soup.find_all("table"):
            for tr in table.find_all("tr"):
                for td in tr.find_all("td"):
                    if td.get_text() in expected_headers:
                        continue
                    data.append(td.get_text())

        for x in data[::3]:
            x_axis.append(int(x))
        for y in data[2::3]:
            y_axis.append(int(y))
        for c in (data[1::3]):
            unicode_char.append(c)

        return {(x_axis[i], y_axis[i]): unicode_char[i] for i in range(max(len(x_axis), len(y_axis)))}
    except TypeError as e:
        print(f"Error parsing data from Google Doc: {e}")
        raise TypeError(f"This is coming from the function fetch_xy_data_from_doc : {e}")


def print_msg(coordinates: dict) -> None:
    """
    Using the dic object add the Unicode symbol to the grid using the cordinates
    :param coordinates: dict object with x and y coordinates and symbol
    :return:
    """
    x = [x[0] for x in list(coordinates.keys())]
    y = [x[1] for x in list(coordinates.keys())]

    max_x = max(x) + 1
    max_y = max(y) + 1
    z = max(max_x, max_y)

    grid = np.full((z,z), fill_value=' ', dtype=str)

    for k, v in coordinates.items():
        grid[max_y - k[1], k[0]] = v

    for row in grid:
        print("".join(row))

def decode_secret_msg(url: str) -> None:
    """
    Main function for decoding secret message
    :param url: Published Google Doc URL
    :return:
    """
    html_content = download_html(url)
    try:
        coordinates_dict = fetch_xy_data_from_doc(html_content)
        print_msg(coordinates_dict)
    except TypeError as e:
        print(f"Error decoding the message from google doc: {e}")

decode_secret_msg("https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pubd")

    # "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub")
    # "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")

