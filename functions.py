import datetime
import os
from json import JSONDecodeError
from typing import Any
from uuid import uuid4

import requests
import urllib3
from tqdm import tqdm

from threadpool import ThreadPool
from worker import worker

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_version(foreign_api_url: str) -> str:
    cookies = {}
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid4()),
        "method": "get_version",
        "params": [],
    }
    response = requests.post(foreign_api_url, json=payload, cookies=cookies)
    return response.json()["result"]["Ok"]["node_version"]


def get_block(foreign_api_url: str, block: int) -> Any:
    cookies = {}
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid4()),
        "method": "get_block",
        "params": [block, None, None],
    }
    response = requests.post(
        foreign_api_url, json=payload, cookies=cookies, timeout=10, verify=False
    )
    try:
        block = response.json()
        if "Err" in block["result"]:
            raise ValueError(block["result"]["Err"])
    except JSONDecodeError as ex:
        raise Exception(response.content)
    return block


def get_status(owner_api_url: str) -> Any:
    cookies = {}
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid4()),
        "method": "get_status",
        "params": [],
    }
    response = requests.post(owner_api_url, json=payload, cookies=cookies)

    return response.json()["result"]["Ok"]


def get_latest_block(owner_api) -> int:
    status = get_status(owner_api)
    return status["tip"]["height"]


def main(latest_block: int, url: str, threads: int):
    # Create folder to store the invalids
    folder = f"./invalids/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.mkdir(folder)

    iterations = latest_block + 1
    for iteration in tqdm(range(1, iterations, threads)):
        pool = ThreadPool(threads)
        for block_number in range(iteration, iteration + threads):
            pool.add_task(worker, url, block_number, folder)
        pool.wait_completion()
