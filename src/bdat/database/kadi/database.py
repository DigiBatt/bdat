import requests

from bdat.database.database.collection import Collection
from bdat.database.database.database import Database
from bdat.database.kadi.collection import KadiCollection


class KadiDatabase(Database):
    url: str
    token: str
    seesion: requests.Session

    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.seesion = requests.Session()

    def __getitem__(self, name: str) -> Collection:
        return KadiCollection(self, name)

    def __getattr__(self, name: str) -> Collection:
        return KadiCollection(self, name)
