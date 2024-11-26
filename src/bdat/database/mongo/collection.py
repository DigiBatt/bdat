import functools
import itertools
import typing
from datetime import datetime

import gridfs
import pymongo
from pymongo.collection import Collection as _C

from bdat.database.database.collection import Collection
from bdat.database.mongo import meta
from bdat.database.storage.resource_id import IdType, ResourceId

if typing.TYPE_CHECKING:
    from bdat.database.storage.storage import DBConfig


class MongoCollection(Collection):
    client: pymongo.MongoClient
    collection: _C
    archive: _C
    dbconfig: "DBConfig"

    def __init__(self, dbconfig: "DBConfig", collection: _C):
        self.dbconfig = dbconfig
        self.client = collection.database.client
        self.collection = collection
        self.archive = collection.database.get_collection(f"_archive_{collection.name}")

    def __make_filter(self, document_id) -> dict:
        dbc = self.dbconfig
        filter = {dbc.id_field: document_id}
        return filter

    @functools.wraps(_C.find_one)
    def find_one(self, document_id, *args, time: datetime | None = None, **kwargs):
        filter = self.__make_filter(document_id)
        if time:
            filter["_meta.date"] = {"$lt": time}
            doc = self.collection.find_one(filter, *args, **kwargs)
            if doc is None:
                filter["_meta.archive_date"] = {"$gt": time}
                doc = self.archive.find_one(filter, *args, **kwargs)
            return doc
        else:
            return self.collection.find_one(filter, *args, **kwargs)

    @functools.wraps(_C.find_one)
    def find_id(self, document_id, *args, time: datetime | None = None, **kwargs):
        filter = self.__make_filter(document_id)
        kwargs["projection"] = {"_id": True}
        doc = None
        if time:
            filter["_meta.date"] = {"$lt": time}
            doc = self.collection.find_one(filter, *args, **kwargs)
            if doc is None:
                filter["_meta.archive_date"] = {"$gt": time}
                doc = self.archive.find_one(filter, *args, **kwargs)
        else:
            doc = self.collection.find_one(filter, *args, **kwargs)
        if doc is None:
            return None
        else:
            return doc["_id"]

    @functools.wraps(_C.find)
    def find(self, filter, *args, time: datetime | None = None, **kwargs):
        if time:
            if filter is None:
                filter = {}
            filter["_meta.date"] = {"$lt": time}
            docs1 = self.collection.find(filter, *args, **kwargs)
            filter["_meta.archive_date"] = {"$gt": time}
            docs2 = self.archive.find(filter, *args, **kwargs)
            return itertools.chain(docs1, docs2)
        else:
            return self.collection.find(filter, *args, **kwargs)

    @functools.wraps(_C.find)
    def find_ids(self, filter, *args, time: datetime | None = None, **kwargs):
        kwargs["projection"] = {"_id": True}
        if time:
            if filter is None:
                filter = {}
            filter["_meta.date"] = {"$lt": time}
            docs1 = self.collection.find(filter, *args, **kwargs)
            filter["_meta.archive_date"] = {"$gt": time}
            docs2 = self.archive.find(filter, *args, **kwargs)
            return (d["_id"] for d in itertools.chain(docs1, docs2))
        else:
            return (d["_id"] for d in self.collection.find(filter, *args, **kwargs))

    @functools.wraps(_C.insert_one)
    def insert_one(self, document, *args, **kwargs):
        self.__replace_links(document)
        meta.add_metadata(document)
        return self.collection.insert_one(document, *args, **kwargs)

    @functools.wraps(_C.insert_many)
    def insert_many(self, documents, *args, **kwargs):
        for doc in documents:
            self.__replace_links(doc)
            meta.add_metadata(doc)
        return self.collection.insert_one(documents, *args, **kwargs)

    @functools.wraps(_C.replace_one)
    def replace_one(self, document_id, replacement, upsert, *args, **kwargs):
        filter = self.__make_filter(document_id)
        self.__replace_links(replacement)
        with self.client.start_session() as session:
            with session.start_transaction():
                old_doc = self.collection.find_one(filter, session=session)
                if old_doc is None:
                    if not upsert:
                        raise Exception("Found no document to replace")
                    meta.add_metadata(replacement)
                else:
                    meta.archive(old_doc, replacement)
                    self.archive.insert_one(old_doc, session=session)
                    self.collection.delete_one({"_id": old_doc["_id"]})
                return self.collection.insert_one(replacement, *args, **kwargs)

    @functools.wraps(_C.count_documents)
    def count_documents(self, *args, **kwargs):
        return self.collection.count_documents(*args, **kwargs)

    @functools.wraps(_C.distinct)
    def distinct(self, *args, **kwargs):
        return self.collection.distinct(*args, **kwargs)

    @functools.wraps(_C.aggregate)
    def aggregate(self, *args, **kwargs):
        return self.collection.aggregate(*args, **kwargs)

    @functools.wraps(_C.delete_one)
    def delete_one(self, document_id):
        filter = self.__make_filter(document_id)
        doc = self.find_one(filter)
        if doc:
            meta.delete(doc)
            with self.client.start_session() as session:
                with session.start_transaction():
                    self.archive.insert_one(doc, session=session)
                    return self.collection.delete_one({"_id": doc["_id"]})

    def get_file(self, file_id):
        filter = self.__make_filter(file_id)
        fs = gridfs.GridFS(self.collection.database, self.collection.name)
        f = fs.find_one(filter)
        return f

    def put_file(
        self, resource_id: IdType, file: typing.IO, name: str, mimetype: str
    ) -> IdType:
        raise NotImplementedError()

    def list_files(self, resource_id: IdType) -> typing.List[str]:
        raise NotImplementedError()

    def delete_file(self, file_id):
        fs = gridfs.GridFS(self.collection.database, self.collection.name)
        fs.delete(file_id)

    def __replace_links(self, document):
        for k, v in document.items():
            if isinstance(v, ResourceId):
                document[k] = v.to_str()
            elif isinstance(v, list):
                if all([isinstance(v2, ResourceId) for v2 in v]):
                    document[k] = [r.to_str() for r in v]

    def query(self, query: typing.Dict | None) -> typing.List[typing.Dict]:
        raise NotImplementedError()

    def query_ids(self, query: typing.Dict | None) -> typing.List[IdType]:
        raise NotImplementedError()
