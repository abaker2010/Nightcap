import json
from typing import Any
from bson import json_util
from bson.objectid import ObjectId

class NightcapJSONDecoder(json.JSONDecoder):
    def decode(self, o: Any) -> Any:
        try:
            return json.loads(o)
        except Exception as e:
            raise Exception(f'Unable to NightcapJSON deserialize data :: {e}')