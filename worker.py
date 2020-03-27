from functions import get_block


def worker(foreign_url: str, block_number: int, folder: str):
    try:
        get_block(foreign_url, block_number)
    except ValueError as ex:
        f = open(f"{folder}/{block_number}.txt", "w+")
        f.write(f"{ex}")
        f.close()
