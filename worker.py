from functions import get_block


def worker(foreign_url: str, block_number: int):
    try:
        get_block(foreign_url, block_number)
    except ValueError as ex:
        return block_number
