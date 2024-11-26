import datetime
from json import JSONEncoder

import numpy as np

from bdat.database.storage.resource_id import ResourceId


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        elif isinstance(obj, ResourceId):
            return obj.to_str()
        elif isinstance(obj, np.int64):
            return int(obj)
        elif obj != obj:
            return None
