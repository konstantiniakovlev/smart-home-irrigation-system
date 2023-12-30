import urequests as requests
from utils import config


def create_url(endpoint="/"):
    base_url = f"http://{config.CONTROLLER_HOST}:{config.CONTROLLER_PORT}"
    return base_url + endpoint


def send_request(url, params=None, json=None, method="get"):
    if method not in ["get", "post"]:
        raise Exception(f"Incorrect request method method used: {method}.")

    if method == "get":
        response = requests.get(url=url, params=params)

    elif method == "post":
        if json is None:
            raise Exception(f"Request body is not provided.")
        response = requests.post(url=url, json=json)

    if response.status_code not in [200, 201]:
        raise Exception(f"{response.status_code}, {response.content}")
