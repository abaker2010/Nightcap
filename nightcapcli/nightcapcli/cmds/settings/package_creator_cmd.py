# region Imports
import traceback
from colorama import Fore
from typing import Dict, List
from nightcapcore.invoker import Invoker
from nightcapcore import TaskManager, Package
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcore.package.params.entry_params import EntryParam
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from nightcapcore.package_creator.package_creator import NightcapPackageCreator
from nightcapcore.printers.subprinters.schemas.dark_schema import TableDarkSchema
from nightcappackages.classes.commands import NightcapPackagePackerCommand, NightcapPackageCreatorCommand
# endregion

class NightcapPacakgeCreatorCMD(NightcapBaseCMD):
    # region Init
    def __init__(self, channelID: str = None) -> None:
        NightcapBaseCMD.__init__(self, ["settings", "package-creator"], channelid=channelID)
        self.task_manager = TaskManager()
        self.package = Package()
        
        #region Testing Data Start
        self._test_data = {
                            "author": {
                                # "creator": "Aaron Baker"
                                "first_name": "Aaron",
                                "last_name": "Baker",
                                "github_url": "https://github.com/abaker2010",
                                "personal_site": None
                            },
                            "package_for": {
                                "module": "github",
                                "submodule": "dns"
                            },
                            "package_information": {
                                "package_name": "dnsrecon",
                                "package_type": "red-team",
                                "version": "1.0",
                                "date": "06/25/2021",
                                "details": "DNSRecon Wrapper",
                                "entry_file": "dnsrecon.py",
                                "language": {
                                    "language": "python",
                                    "version": "3.8",
                                    "env_name": "None",
                                    "requirements_file": "requirements.txt",
                                    "requirements": {
                                        "art" : '1.4.4'
                                    }
                                },
                                "github": {
                                    "url": "https://github.com/darkoperator/dnsrecon/archive/refs/heads/master.zip"
                                },
                                "entry_file_optional_params": {
                                    "0": {
                                        "name": "domain",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-d",
                                        "description": "Domain",
                                        "param_needed": "True",
                                        "required": "True"
                                    },
                                    "1": {
                                        "name": "ns_server",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-n",
                                        "description": "NS Server",
                                        "param_needed": "True"
                                    },
                                    "2": {
                                        "name": "range",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-r",
                                        "description": "IP Range",
                                        "param_needed": "True"
                                    },
                                    "3": {
                                        "name": "dictionary",
                                        "value": "None",
                                        "corresponding_flag": "-D",
                                        "description": "Dictionary file of subdomain and hostnames to use for brute force",
                                        "param_needed": "True"
                                    },
                                    "4": {
                                        "name": "filiter",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-f",
                                        "description": "Filter out of brute force domain lookup, records that resolve to the wildcard defined IP address when saving records.",
                                        "param_needed": "True"
                                    },
                                    "5": {
                                        "name": "type",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-t",
                                        "description": "Type of enumeration to perform.",
                                        "param_needed": "True"
                                    },
                                    "6": {
                                        "name": "axfr",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-a",
                                        "description": "Perform AXFR with standard enumeration.",
                                        "param_needed": "False"
                                    },
                                    "7": {
                                        "name": "reverse_lookup",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-s",
                                        "description": "Perform a reverse lookup of IPv4 ranges in the SPF record with standard enumeration.",
                                        "param_needed": "False"
                                    },
                                    "8": {
                                        "name": "google",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-g",
                                        "description": "Perform Google enumeration with standard enumeration.",
                                        "param_needed": "False"
                                    },
                                    "10": {
                                        "name": "crt_enum",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-k",
                                        "description": "Perform crt.sh enumeration with standard enumeration.",
                                        "param_needed": "False"
                                    },
                                    "11": {
                                        "name": "whois_lookup",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-w",
                                        "description": "Perform deep whois record analysis and reverse lookup of IP ranges found through Whois when doing a standard enumeration.",
                                        "param_needed": "False"
                                    },
                                    "12": {
                                        "name": "dnssec",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-z",
                                        "description": "Performs a DNSSEC zone walk with standard enumeration.",
                                        "param_needed": "False"
                                    },
                                    "13": {
                                        "name": "threads",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "--threads",
                                        "description": "Number of threads to use in reverse lookups, forward lookups, brute force and SRV record enumeration.",
                                        "param_needed": "True"
                                    },
                                    "14": {
                                        "name": "lifetime",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "--lifetime",
                                        "description": "Time to wait for a server to response to a query.",
                                        "param_needed": "True"
                                    },
                                    "15": {
                                        "name": "use_tcp",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "--tcp",
                                        "description": "Use TCP protocol to make queries.",
                                        "param_needed": "False"
                                    },
                                    "16": {
                                        "name": "sqllite_file",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "--db",
                                        "description": "SQLite 3 file to save found records.",
                                        "param_needed": "True"
                                    },
                                    "17": {
                                        "name": "xml_file",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-x",
                                        "description": "XML file to save found records.",
                                        "param_needed": "True"
                                    },
                                    "18": {
                                        "name": "csv_file",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-c",
                                        "description": "Comma separated value file.",
                                        "param_needed": "True"
                                    },
                                    "19": {
                                        "name": "json_file",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-j",
                                        "description": "JSON file.",
                                        "param_needed": "True"
                                    },
                                    "20": {
                                        "name": "wildcard",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "--iw",
                                        "description": "Continue brute forcing a domain even if a wildcard records are discovered.",
                                        "param_needed": "False"
                                    },
                                    "21": {
                                        "name": "verbose",
                                        "value": "None",
                                        "default": "None",
                                        "corresponding_flag": "-v",
                                        "description": "Enable verbose in script",
                                        "param_needed": "False"
                                    }
                                },
                                "uid": "f2115db006a47334168ecabe9ce2108a4a177bc134ae56c4b27563989facf506"
                            }
                        }
        # endregion

        self.package = Package(self._test_data)
        self.package_creator = NightcapPackageCreator(self.package)
    # endregion 
    
    def cmdloop(self) -> None:
        ScreenHelper().clearScr()
        _format = "%s\n\t%s\n"
        _header_format = "\n\t\t\t%s\n\t\t\t* %s *\n\t\t\t%s\n"

        _title = "Package Creator"

        _header_lines = "*" * (len(_title)+4) 
        _header = _header_format % (_header_lines, _title, _header_lines)
        
        _body = "Build custom Nightcap packages (.ncp) files to share \
                \n\twith other and enhance the utilities available.\
                \n\n\tFor details about what needs to be filled in use, \
                \n\tthe options command and set command to fill in \
                \n\tthe required details."

        intro = (_format % (_header, _body))
        return super().cmdloop(intro)
    
    #region Options Section Start
    def help_options(self) -> None:
        # self.printer.help("Options/Parameters available for package creation")
        self.printer.item_2(
            "Options/Parameters available for package creation",
            leadingTab=1,
            vtabs=1,
            leadingText="",
            endingBreaks=1,
            textColor=Fore.LIGHTGREEN_EX,
        )

    def do_options(self, line) -> None:
        try:
            _options:Dict = self.package.__dict__
        
            _author_data = {'Parameter' : [], "Value" : []}
            _general_data = {'Parameter' : [], "Value" : []}
            _package_for_data = {'Parameter' : [], "Value" : []}


            _lang_requirements = {'Package' : [], 'Version' : []}
            _optional_params = {'Name' : [], 'Default' : [], 'Flag' : [], 'Param Needed' : [], 'Required' : [], 'Description' : []}

            # set up options
            _author_data['Parameter'].append('First Name')
            _author_data['Parameter'].append('Last Name')
            _author_data['Parameter'].append('Github URL')
            _author_data['Parameter'].append('Personal Site')

            _general_data['Parameter'].append('Name')
            _general_data['Parameter'].append('Type')
            _general_data['Parameter'].append('Version')

            _package_for_data['Parameter'].append('Module')
            _package_for_data['Parameter'].append('Submodule')

            _general_data['Parameter'].append('Details')
            _general_data['Parameter'].append('Entry File')
            _general_data['Parameter'].append('Github')
            _general_data['Parameter'].append('Entry Class')
            _general_data['Parameter'].append('Language')
            _general_data['Parameter'].append('Language Version')
            _general_data['Parameter'].append('Env Name')
            _general_data['Parameter'].append('Language Requirements')
            _general_data['Parameter'].append('Optional Params')

            # set up matching option -> values
            _author_data['Value'].append(str(_options['author'].first_name))
            _author_data['Value'].append(str(_options['author'].last_name))
            _author_data['Value'].append(str(_options['author'].github_url))
            _author_data['Value'].append(str(_options['author'].personal_site))

            _general_data['Value'].append(str(_options['package_information'].package_name))
            _general_data['Value'].append(str(_options['package_information'].package_type))
            _general_data['Value'].append(str(_options['package_information'].version))

            _package_for_data['Value'].append(str(_options['package_for'].module))
            _package_for_data['Value'].append(str(_options['package_for'].submodule))

            _general_data['Value'].append(str(_options['package_information'].details))
            _general_data['Value'].append(str(_options['package_information'].entry_file))
            _general_data['Value'].append(str(_options['package_information'].github.url))
            _general_data['Value'].append(str(_options['package_information'].entry_class_name))
            _general_data['Value'].append(str(_options['package_information'].language.language))
            _general_data['Value'].append(str(_options['package_information'].language.version))
            _general_data['Value'].append(str(_options['package_information'].language.env_name))
            _general_data['Value'].append(str('NO' if _options['package_information'].language.requirements == None and _options['package_information'].language.requirements_file == None else 'YES'))
            _general_data['Value'].append(str('NO' if _options['package_information'].entry_file_optional_params == None else 'YES'))

            # generate Language Requirement data
            if _options['package_information'].language.requirements_file != None:
                _lang_requirements['Package'].append("Requirements File")
                _lang_requirements['Version'].append(_options['package_information'].language.requirements_file)
            else:
                if _options['package_information'].language.requirements != None:
                    for pkg_name, pkg_version in _options['package_information'].language.requirements.items():
                        _lang_requirements['Package'].append(pkg_name)
                        _lang_requirements['Version'].append(pkg_version)

            # generate Optional Params data
            # _optional_params = {'Value' : [], 'Default' : [], 'Flag' : [], 'Param Needed' : [], 'Required' : [], 'Description' : []}
            if _options['package_information'].entry_file_optional_params != None:
                _params:Dict[str, EntryParam] = _options['package_information'].entry_file_optional_params.items()
                for k, v in _params:
                    _optional_params['Name'].append(str(v.name))
                    _optional_params['Default'].append(str(v.default))
                    _optional_params['Flag'].append(str(v.corresponding_flag))
                    _optional_params['Param Needed'].append(str(v.param_needed))
                    _optional_params['Required'].append(str(v.required))
                    _optional_params['Description'].append(str(v.description))

            # Print Table(s)
            self.printer.print_underlined_header("Author Information")
            self.printer.table(data=_author_data, newlines_before_table=0)

            self.printer.print_underlined_header("Module/Submodule Information")
            self.printer.table(data=_package_for_data, newlines_before_table=0)

            self.printer.print_underlined_header("General Information")
            self.printer.table(data=_general_data, newlines_before_table=0)

            if _options['package_information'].language.requirements_file != None:
                self.printer.print_underlined_header("Language Requirements")
                self.printer.table(data=_lang_requirements, newlines_before_table=0)

            elif _options['package_information'].language.requirements != None:
                self.printer.print_underlined_header("Language Requirements")
                self.printer.table(data=_lang_requirements, newlines_before_table=0)

            if _options['package_information'].entry_file_optional_params != None:
                self.printer.print_underlined_header("Optional Params")
                self.printer.table(data=_optional_params, newlines_before_table=0, schema=TableDarkSchema(column_count=6))
            # Package Options End
        except Exception as e:
            self.printer.print_error(e)
            print(traceback.print_exc())
    #endregion Options Section End

    #region Set Option Start
    def help_set(self) -> None:
        self.printer.item_2(
            "set default parameter",
            "set [PARAM] [SUB-PARAM]",
            leadingTab=1,
            vtabs=1,
            leadingText="",
            endingBreaks=1,
            textColor=Fore.LIGHTGREEN_EX,
        )
        self.printer.item_2(
            "NOTE",
            "No value is needed at the end, there will be a guided process of entering the information",
            leadingTab=1,
            vtabs=1,
            leadingText="",
            endingBreaks=1,
            textColor=Fore.LIGHTGREEN_EX,
        )

    def do_set(self, line) -> None:
        _options = line.split(" ")
        try:
            self.package_creator.modify_package(_options[0], _options[1])
        except IndexError as index:
            self.printer.print_error(Exception("Please finish the set command :: set [module] [submodule]"))
        except Exception as e:
            self.printer.print_error(e)

    def complete_set(self, text, line, begidx, endidx) -> List[str]:
        _options:Dict = self.package.__dict__
        _split = line.split(' ')

        if len(_split) == 2:
            _ = ["author", "package_information", "package_for", "creator"]
            if _split[1] not in _:
                return [i for i in _ if i.startswith(text)]
            else:
                print("Is in")
                _ = _options[_split[1]].__dict__.keys()
                print("New Options")
                print(str(_))
                return [i for i in _ if i.startswith(text)]
        elif len(_split) == 3:
            _ = _options[_split[1]].__dict__.keys()
            return [i for i in _ if i.startswith(text)]

    #endregion Set Option End

    def help_create(self) -> None:
        self.printer.help("Build out the new NCP file.")
    
    def do_create(self, line) -> None:
        try:
            self.printer.print_underlined_header("Please Review The Setting For The Package")
            self.do_options(None)
            
            _ready = self.printer.input("Ready to create? (Y/n)", defaultReturn=True)
            
            if _ready:
                ScreenHelper().clearScr()
                invoker = Invoker()
                invoker.set_on_start(NightcapPackageCreatorCommand(self.package_creator.package))
                _tmp_path = invoker.execute()
                invoker.set_on_start(NightcapPackagePackerCommand(_tmp_path))
                invoker.execute()
        except Exception as e:
            self.printer.print_error(f"ERROR CREATING PACKAGE :: {e}")
            self.printer.print_error(traceback.print_exc())
            
