import functools
import typing

from pymongo.database import Database as _D

from bdat.database.database.collection import Collection
from bdat.database.database.database import Database
from bdat.database.mongo.collection import MongoCollection

if typing.TYPE_CHECKING:
    from bdat.database.storage.storage import DBConfig


class MongoDatabase(Database):
    database: _D
    dbconfig: "DBConfig"

    def __init__(self, dbconfig: "DBConfig", database: _D):
        self.dbconfig = dbconfig
        self.database = database

    @functools.wraps(_D.__getitem__)
    def __getitem__(self, name: str) -> Collection:
        return MongoCollection(self.dbconfig, self.database.__getitem__(name))

    @functools.wraps(_D.__getattr__)
    def __getattr__(self, name: str) -> Collection:
        return MongoCollection(self.dbconfig, self.database.__getattr__(name))
