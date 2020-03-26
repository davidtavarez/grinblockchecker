import argparse
import datetime
from typing import Any
from uuid import uuid4

import requests


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
    block = requests.post(foreign_api_url, json=payload).json()
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--protocol", help="API Protocol, default: http", default="http",
    )
    parser.add_argument(
        "-a",
        "--address",
        help="Node API IP/Hostname, default: 127.0.0.1",
        default="127.0.0.1",
    )
    parser.add_argument(
        "-o", "--port", help="Node API Port, default: 3413", default="3413",
    )
    args = parser.parse_args()

    foreign_url = f"{args.protocol}://{args.address}:" f"{args.port}/v2/foreign"
    owner_url = f"{args.protocol}://{args.address}:" f"{args.port}/v2/owner"

    blocks_with_errors: [int] = []
    latest_block = get_latest_block(owner_url)
    for block_number in range(1, latest_block + 1):
        try:
            block_information = get_block(foreign_url, latest_block)
            print(f"Block found: {block_number}")
        except ValueError as ex:
            blocks_with_errors.append(block_number)
            print(f"Error with block {block_number}: {ex}")

    ts = datetime.datetime.now().timestamp()
    f = open(f"{ts}.txt", "w+")
    for block_number in blocks_with_errors:
        f.write(f"{block_number}\n")
    f.close()
