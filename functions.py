from typing import Any
from uuid import uuid4

import requests

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_version(foreign_api_url: str) -> str:
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid4()),
        "method": "get_version",
        "params": [],
    }
    response = requests.post(foreign_api_url, json=payload)
    return response.json()["result"]["Ok"]["node_version"]


def get_block(foreign_api_url: str, block: int) -> Any:
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid4()),
        "method": "get_block",
        "params": [block, None, None],
    }
    response = requests.post(
        foreign_api_url, json=payload, timeout=5, verify=False
    )
    block = response.json()
    if "Err" in block["result"]:
        raise ValueError(block["result"]["Err"])
    return block


def get_status(owner_api_url: str) -> Any:
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid4()),
        "method": "get_status",
        "params": [],
    }
    response = requests.post(owner_api_url, json=payload)

    return response.json()["result"]["Ok"]


def get_latest_block(owner_api) -> int:
    status = get_status(owner_api)
    return status["tip"]["height"]
