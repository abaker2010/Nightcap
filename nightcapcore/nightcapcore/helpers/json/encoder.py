import json
from typing import Any
from bson import json_util
from bson.objectid import ObjectId

class NightcapJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
                return str(o)
        elif hasattr(o, 'to_json'):
            return o.to_json()
        else:
            raise TypeError('Object of type %s with value of %s is not NightcapJSON serializable' % (type(o), repr(o)))
   
