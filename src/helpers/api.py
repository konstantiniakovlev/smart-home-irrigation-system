import utils.app_config as config
from fastapi import FastAPI, HTTPException
from typing import Union, Optional
import requests
from pydantic import BaseModel

RELAY_ON = "/relay/on"


def get_device_params(device_id: Union[int, str]):
    for param_config in config.DEVICE_PARAMETER_CONFIGS:
        if param_config["id"] == int(device_id):
            return param_config
    raise HTTPException(status_code=404, detail="Device not found")


def get_params(device_params: dict, duration: int = None):

    if duration is not None:
        params = {"duration": duration}
    elif device_params.get("optimal_duration", None) is not None:
        params = {"duration": device_params["optimal_duration"]}
    else:
        params = {}

    return params


def get_response(
        url: str,
        params: Optional[dict] = None,
        request_type: Optional[str] = "get"
):
    request = requests.get
    request = requests.post if request_type == "post" else request

    try:
        response = request(url, params=params)
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=404, detail="Device could not be reached")

    if response.status_code not in [200, 201]:
        if response.status_code == 403:
            raise HTTPException(status_code=response.status_code, detail="IP address could not be reached")
        raise HTTPException(status_code=response.status_code, detail=response.reason)
    return response


app = FastAPI(**config.APP_PARAMETER_CONFIGS)


@app.get(
    path="/devices/{device_id}/run/",
    summary="Run Single Device",
    description="Run a single pump for specified or optimal amount of time."
)
def run_pump(
        device_id: Union[int, str],
        duration: int = None
):
    device_params = get_device_params(device_id)
    params = get_params(device_params, duration)

    base_url = f"http://{device_params.get('ip', '')}:{device_params.get('port', '')}/"
    url = base_url + RELAY_ON

    response = get_response(url=url, params=params)
    return response.json()


@app.get(
    path="/devices/run/",
    summary="Run All Devices Simultaneously",
    description="Run all pumps for specified or optimal amount of time."
)
def run_all_pumps(duration: int = None):
    responses = []
    for device_params in config.DEVICE_PARAMETER_CONFIGS:
        params = get_params(device_params, duration)

        base_url = f"http://{device_params.get('ip', '')}:{device_params.get('port', '')}/"
        url = base_url + RELAY_ON

        response = get_response(url, params=params)
        responses.append(response.json())
    return 200, responses

# class Item(BaseModel):
#     name: str
#     surname: str
#     favourite_dessert: str
#
#
# @app.post("/give_name/")
# def receive_name(payload: Item):
#     print(payload)
