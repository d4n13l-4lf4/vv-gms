from tinydb import TinyDB


def create_db(filename: str):
    db = TinyDB(filename)
    return db