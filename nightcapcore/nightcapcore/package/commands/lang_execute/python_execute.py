from nightcapcore import Command
from nightcapcore.package.package import Package
from nightcapcore.subprocess import CustomSubprocess
from nightcapcore.exceptions.virtenv import VirtenvCheckException
from nightcapcore.environment_support import PyenvChecks
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase

class PythonPackageExecuteCommand(Command):
    def __init__(self, package: Package, database: MongoPackagesDatabase) -> None:
        super().__init__()
        self.package = package
        self.database = database
    
    def execute(self) -> dict:
        exe_path = self.database.get_package_run_path(self.package)
        _flags_dic = {}
        _flags = ""

        for k, v in self.package.package_information.entry_file_optional_params.items():
            if v.required == True:
                if (v.value == "None" and v.default == "None") or (v.value == "None"):
                    raise Exception("Required Param :: " + str(v.name))
                else:
                    _flags_dic[v.corresponding_flag] = v.value if v.value != "None" else v.default
            elif v.value != "None":
                _flags_dic[v.corresponding_flag] = v.value
            elif v.default != "None":
                _flags_dic[v.corresponding_flag] = v.default

        for k, v in _flags_dic.items():
            _flags += "%s %s " % (k, v)
        
        if self.package.package_information.language.language.lower() == "python":
            _pyenv_checks = PyenvChecks()

            if _pyenv_checks.check_env(self.package.package_information.language.env_name):
                call = "%s %s %s %s %s %s %s" % (
                        "pyenv",
                        "do",
                        "-e",
                        str(self.package.package_information.language.env_name),
                        str(self.package.package_information.language.language),
                        exe_path,
                        _flags.strip()
                    )

                cmd = call.split(' ')
                _return_data = CustomSubprocess(cmd).execute()
                return _return_data
            else:
                raise VirtenvCheckException("PYENV FAILED :: NO ENVIRONMENT FOR PACKAGE")
        else:
            raise Exception("NEED TO IMPLEMENT OTHER LANGUAGE SETUP")