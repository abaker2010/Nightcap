# region Import
from typing import List
from uuid import uuid4
from nightcapcore.package.package import Package
from nightcapcli.observer import CLISubscriber, CLIBroker
from nightcapcli.validators.cmd_validator import CMDValidate
from nightcapcli.cmds.main_cmd import NightcapMainCMD
from nightcapcli.cmds.package.package_cmd import NightcapCLIPackageCMD
from nightcapcore.exceptions.publisher import PublisherValidationException
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
# endregion

class Nightcap(NightcapMainCMD):
    """
    This object is used to create the CLI's for the users:
        - Base
        - Module
        - Submodule

    Init:
        - selected list         :  used for [<T>][<T>] options for console
        - channelid             :  used for the (self) notifications from the observer
        - parentid              :  used for the parent interactive notifications from the observer
        - additionalchildren    :  used for additional page creation when a deep path is specified
    """

    def __init__(
        self,
        selected: list,
        channelid: str = "",
        parentid: str = "",
    ) -> None:
        NightcapMainCMD.__init__(self, selected, channelid)
        self.channelid = channelid
        self.parentid = parentid
        self.packages_db = MongoPackagesDatabase()
        CLISubscriber('basecli', CLIBroker(), self._callback)

    def new_channel(self) -> str:
        _uid = uuid4().hex
        if _uid not in dict(self.channels).keys():
            self.channels[_uid] = dict()
            return _uid
        else:
            self.new_channel()

    # region Get package config
    def get_package_config(self, path: list) -> Package:
        try:
            self.pkg_conf = self.packages_db.get_package_config(path)
            return Package(self.pkg_conf)
        except Exception as e:
            raise Exception("Error with getting package :: %s" % e)
    # endregion


    def _callback(self, msg):
        try:
            _msg:dict = msg
            _pages:List[str] = _msg['page_add']

            _validate = CMDValidate(self.selectedList).validate(_pages)

            if _validate[0] == True:
                self.selectedList = _validate[1]

                if len(self.selectedList) == 3:
                    _channel = self.new_channel()
                    _package_cmd = NightcapCLIPackageCMD(
                        self.selectedList,
                        self.get_package_config(
                            self.selectedList
                        ),
                        _channel,
                    )
                    _package_cmd.cmdloop()

                    if _package_cmd.postloop():
                        self.selectedList.pop()
                        NightcapMainCMD.__init__(self, self.selectedList, self.channelid)
                    return True
                elif len(self.selectedList) < 3:
                    NightcapMainCMD.__init__(self, self.selectedList, self.channelid)
                    return True
                else:
                    raise PublisherValidationException(f"FAILED TO FIND CORRECT ROUTE :: {_validate}")
        except Exception as e:
            raise e