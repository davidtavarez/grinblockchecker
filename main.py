import argparse

from functions import get_latest_block, main

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
        "-t", "--threads", help="Number of threads, default: 10", default=2,
    )
    args = parser.parse_args()

    main(
        get_latest_block(
            f"{args.protocol}://{args.address}:" f"{args.port}/v2/owner"
        ),
        f"{args.protocol}://{args.address}:" f"{args.port}/v2/foreign",
        int(args.threads),
    )
