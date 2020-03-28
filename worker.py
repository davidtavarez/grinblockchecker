def worker(foreign_url: str, block_number: int, folder: str):
    from functions import get_block

    try:
        get_block(foreign_url, block_number)
    except Exception as ex:
        f = open(f"{folder}/{block_number}.txt", "w+")
        f.write(f"{ex}")
        f.close()
