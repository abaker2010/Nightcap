from typing import Dict, List
from nightcapcore.package.filters.base.filter import Filter

class ReturnFilters(object):
    def __init__(self, return_filters: Dict[str, List[Filter]] = None) -> None:
        self.return_filters:List[Filter] = return_filters

    def to_json(self):
        return self.return_filters