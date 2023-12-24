from fastapi import FastAPI, HTTPException
from typing import Union, Optional
import requests
from pydantic import BaseModel, Field
from utils.app_config import *
from utils.queries import *
from helpers.db import DataBase

RELAY_ON = "relay/on"
DEVICES_TAG = "Devices"


def get_db_response(db, query, fetch, commit=False):
    try:
        response = db.execute(query, fetch=fetch, commit=commit)
    except ConnectionError as e:
        raise HTTPException(status_code=404, detail=e)

    return response


def get_api_response(
        url: str,
        params: Optional[dict] = None,
        request_type: Optional[str] = "get"
) -> requests.Response:
    request = requests.get
    request = requests.post if request_type == "post" else request

    try:
        response = request(url, params=params)
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=404, detail=f"Device could not be reached. URL: {url}")
    except requests.exceptions.InvalidURL:
        raise HTTPException(status_code=404, detail=f"InvalidURL: {url}")

    if response.status_code not in [200, 201]:
        if response.status_code == 403:
            raise HTTPException(status_code=response.status_code, detail="IP address could not be reached")
        raise HTTPException(status_code=response.status_code, detail=response.reason)
    return response


app = FastAPI(**APP_PARAMETER_CONFIGS)


@app.get(
    path="/devices/",
    summary="Get Configuration Parameters of Every Device",
    description="Receive configuration parameters for all devices currently set up in house.",
    tags=[DEVICES_TAG]
)
def return_devices() -> list:
    query = get_devices_query
    db = DataBase(name="smart-home-postgres")
    response = get_db_response(db, query, fetch=True, commit=False)
    db.close()
    return response


@app.get(
    path="/devices/run/",
    summary="Run All Devices Simultaneously",
    description="Run all pumps for specified or optimal amount of time.",
    tags=[DEVICES_TAG]
)
def run_all_pumps(duration: int = None) -> list:
    responses = []
    device_params = [device for device in return_devices() if device["device_type"] == "Raspberry Pi Pico W"]
    params = [{"duration": duration}] if duration else [{} for _ in range(len(device_params))]

    for idx in range(len(device_params)):
        ip_address = device_params[idx].get('ip_address', '/32').split('/')[0]
        port = device_params[idx].get('port', '')

        base_url = f"http://{ip_address}:{port}/"
        url = base_url + RELAY_ON

        response = get_api_response(url=url, params=params[idx])
        responses.append(response.json())

    return responses


@app.get(
    path="/devices/{device_id}/",
    summary="Get Configuration Parameters of Single Device",
    description="Receive configuration parameters for one specified device currently set up in house.",
    tags=[DEVICES_TAG]
)
def return_device(device_id: Union[int, str]) -> list:
    query = get_device_query % {"device_id": device_id}
    db = DataBase(name="smart-home-postgres")
    response = get_db_response(db, query, fetch=True, commit=False)
    db.close()
    return response


@app.get(
    path="/devices/{device_id}/run/",
    summary="Run Single Device",
    description="Run a single pump for specified or optimal amount of time.",
    tags=[DEVICES_TAG]
)
def run_pump(
        device_id: Union[int, str],
        duration: int = None
) -> dict:
    device_params = return_device(device_id=device_id)
    device_params = device_params[0] if len(device_params) > 0 else {}
    params = {"duration": duration} if duration else {}

    ip_address = device_params.get('ip_address', '/32').split('/')[0]
    port = device_params.get('port', '')

    base_url = f"http://{ip_address}:{port}/"
    url = base_url + RELAY_ON

    response = get_api_response(url=url, params=params)
    return response.json()


class DeviceInfo(BaseModel):
    mac_address: str
    ip_address: str
    device_type: str
    port: int
    device_description: Union[str, None] = Field(default=None)
    program_description: Union[str, None] = Field(default=None)


@app.post(
    path="/devices/register/",
    summary="Register Device in Database",
    description="Register the device using their mac address. If the address already exists, other fields will be updated.",
    tags=[DEVICES_TAG]
)
def register_device(payload: DeviceInfo) -> int:
    db = DataBase(name="smart-home-postgres")

    rd_query = register_device_query % {
        'mac_address': payload.mac_address,
        'ip_address': payload.ip_address,
        'device_type': payload.device_type,
        'description': payload.device_description,
    }
    response = get_db_response(db, rd_query, fetch=True, commit=True)
    device_id = response[0]["device_id"]

    rp_query = register_program_query % {
        'device_id': device_id,
        'port': payload.port,
        'description': payload.program_description
    }
    get_db_response(db, rp_query, fetch=False, commit=True)
    db.close()

    return device_id
