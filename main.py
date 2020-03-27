import argparse
import datetime
import os

from tqdm import tqdm

from functions import get_latest_block
from threadpool import ThreadPool
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

    # Create folder to store the invalids
    folder = f"./invalids/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.mkdir(folder)

    owner_url = f"{args.protocol}://{args.address}:" f"{args.port}/v2/owner"
    latest_block = get_latest_block(owner_url)

    foreign_url = f"{args.protocol}://{args.address}:" f"{args.port}/v2/foreign"

    threads = int(args.threads)
    iterations = latest_block + 1
    for iteration in tqdm(range(1, iterations, threads)):
        pool = ThreadPool(threads)
        for block_number in range(iteration, iteration + threads):
            pool.add_task(worker, foreign_url, block_number, folder)
        pool.wait_completion()
