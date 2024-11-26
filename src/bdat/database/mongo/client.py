import functools
import typing

from pymongo import MongoClient as _M

from bdat.database.database.database import Database
from bdat.database.mongo.database import MongoDatabase

if typing.TYPE_CHECKING:
    from bdat.database.storage.storage import DBConfig


class MongoClient:
    client: _M
    dbconfig: "DBConfig"

    @functools.wraps(_M.__init__)
    def __init__(self, dbconfig, *args, **kwargs):
        self.client = _M(*args, **kwargs)
        self.dbconfig = dbconfig

    @functools.wraps(_M.__getitem__)
    def __getitem__(self, name: str) -> Database:
        return MongoDatabase(self.dbconfig, self.client.__getitem__(name))

    @functools.wraps(_M.__getattr__)
    def __getattr__(self, name: str) -> Database:
        return MongoDatabase(self.dbconfig, self.client.__getattr__(name))
