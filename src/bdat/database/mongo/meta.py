import getpass
from datetime import datetime

import bson

username = getpass.getuser()


def add_metadata(doc: dict, version: int = 1):
    doc["_meta"] = {
        "creator": username,
        "date": datetime.utcnow(),
        "version": version,
    }


def archive(old: dict, new: dict):
    if not "_id" in new:
        new["_id"] = bson.ObjectId()
    add_metadata(new, old["_meta"]["version"] + 1)
    old.setdefault("_meta", {})["next"] = new["_id"]
    new["_meta"]["previous"] = old["_id"]
    old["_meta"]["archive_date"] = datetime.utcnow()


def delete(old: dict):
    old.setdefault("_meta", {})["archive_date"] = datetime.utcnow()
