import argparse
import concurrent.futures as futures
import datetime

from tqdm import tqdm

from functions import get_latest_block
from worker import worker

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
    parser.add_argument(
        "-t", "--threads", help="Number of threads, default: 10", default=10,
    )
    args = parser.parse_args()

    owner_url = f"{args.protocol}://{args.address}:" f"{args.port}/v2/owner"
    latest_block = get_latest_block(owner_url)

    file_name = f"{datetime.datetime.now().timestamp()}.txt"
    foreign_url = f"{args.protocol}://{args.address}:" f"{args.port}/v2/foreign"

    blocks_with_errors: [int] = []
    for block_number in tqdm(range(1, latest_block + 1)):
        with futures.ThreadPoolExecutor(int(args.threads)) as executor:
            invalid_block = executor.submit(
                worker, foreign_url, block_number
            ).result()
            if invalid_block:
                blocks_with_errors.append(invalid_block)

    if len(blocks_with_errors):
        ts = datetime.datetime.now().timestamp()
        f = open(f"{file_name}", "w+")
        for block_number in blocks_with_errors:
            f.write(f"{block_number}\n")
        f.close()
