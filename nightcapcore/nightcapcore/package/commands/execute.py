from pydoc import locate
from typing import List, Tuple
from nightcapcore import Command
from nightcapcore import PkgInvoker
from nightcapcore.invoker import Invoker
from nightcapcore.lang_supported.enum.lang_enum import LangEnum
from nightcapcore.package.package import Package
from nightcapcore.subprocess import CustomSubprocess
from nightcapcore.environment_support import PyenvChecks
from nightcapcore.exceptions.virtenv import VirtenvCheckException
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from .lang_execute.python_execute import PythonPackageExecuteCommand
from .lang_execute.go_execute import GoPackageExecuteCommand

class PackageExecuteCommand(Command):
    def __init__(self, package: Package, database: MongoPackagesDatabase) -> None:
        self.package = package
        self.database = database

    def execute(self) -> Tuple[int, List[str]]:
        try:
            # if self.package.package_information.github.url == None:
            #         print("Was installed from github")
            #         # region Github Package 
            #         exe_path = self.database.get_package_run_path(self.package)
            #         dynamic_class = locate(exe_path)
            #         _invoker = PkgInvoker()
            #         try:
            #             _params = {}
            #             for k, v in self.package.package_information.entry_file_optional_params.items():
            #                 _params[v.name] = v.value
            #             _invoker.set_on_start(dynamic_class(_params))
            #             _invoker.set_on_finish(dynamic_class(_params))
            #             _invoker.execute()
            #             return True
            #         except Exception as e:
            #             raise Exception("ERROR EXECUTING CUSTOME :: %s" % e)
            #         # endregion

            # else:
            if str(self.package.package_information.language.language).lower() == str(LangEnum.PYTHON):
                try:
                    invoker = Invoker()
                    invoker.set_on_start(PythonPackageExecuteCommand(self.package, self.database))
                    return invoker.execute()
                except Exception as e:
                    raise Exception("ERROR WITH PACKAGE EXECUTION (PYTHON) :: %s" % (str(e)))
            elif str(self.package.package_information.language.language).lower() == str(LangEnum.GO):
                try:
                    invoker = Invoker()
                    invoker.set_on_start(GoPackageExecuteCommand(self.package, self.database))
                    return invoker.execute()
                except Exception as e:
                    raise Exception("ERROR WITH PACKAGE EXECUTION (GO) :: %s" % (str(e)))
            else:
                raise Exception("NEED TO IMPLEMENT OTHER LANGUAGE SETUP")
            # region Not Github Package
            # exe_path = self.database.get_package_run_path(self.package)
            # _flags_dic = {}
            # _flags = ""

            # for k, v in self.package.package_information.entry_file_optional_params.items():
            #     if v.required == True:
            #         if (v.value == "None" and v.default == "None") or (v.value == "None"):
            #             raise Exception("Required Param :: " + str(v.name))
            #         else:
            #             _flags_dic[v.corresponding_flag] = v.value if v.value != "None" else v.default
            #     elif v.value != "None":
            #         _flags_dic[v.corresponding_flag] = v.value
            #     elif v.default != "None":
            #         _flags_dic[v.corresponding_flag] = v.default

            # for k, v in _flags_dic.items():
            #     _flags += "%s %s " % (k, v)
            
            # if self.package.package_information.language.language.lower() == "python":
            #     _pyenv_checks = PyenvChecks()

            #     if _pyenv_checks.check_env(self.package.package_information.language.env_name):
            #         call = "%s %s %s %s %s %s %s" % (
            #                 "pyenv",
            #                 "do",
            #                 "-e",
            #                 str(self.package.package_information.language.env_name),
            #                 str(self.package.package_information.language.language),
            #                 exe_path,
            #                 _flags.strip()
            #             )

            #         cmd = call.split(' ')
            #         _return_data = CustomSubprocess(cmd).execute()
            #         return _return_data
            #     else:
            #         raise PyenvEnvCheckException("PYENV FAILED :: NO ENVIRONMENT FOR PACKAGE")
            # else:
            #     raise Exception("NEED TO IMPLEMENT OTHER LANGUAGE SETUP")
                # endregion

                # else:
                #     try:
                #         call = "%s%s %s %s" % (
                #                 str(self.package.package_information.language.language),
                #                 str(self.package.package_information.language.version),
                #                 exe_path,
                #                 _flags.strip()
                #             )

                #         cmd = call.split(' ')
                #         _return_data = CustomSubprocess(cmd).execute()
                #         return _return_data

                #     except Exception as e:
                #         raise Exception("ERROR WITH EXECUTION :: %s" % e)

        except Exception as e:
            raise e