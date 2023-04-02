from typing import List
from nightcapcore.projects.projects import Project
from nightcapcli.mixins.cmd_parts.base import CMDPartBase
from nightcapcore.configuration import NightcapCLIConfiguration
from nightcapcore.database.mongo.mongo_projects import MongoProjectsDatabase

class ProjectsCMDPart(CMDPartBase):
    def __init__(self, selectedList: List[str] = None) -> None:
        super().__init__()
        self.selectedList = selectedList
        self.projects_db = MongoProjectsDatabase()
        self.conf = NightcapCLIConfiguration()

    #region Complete Projects
    def complete_projects(self, text, line, begidx, endidx) -> List[str]:
        try:

            _split:List[str] = line.split(" ")
            _options = []

            if len(_split) == 2:
                _options = ["create", "delete", "deselect", "list", "select"]
            else:
                if _split[1] == "select" or _split[1] == "delete":
                    for proj in self.projects_db.list_projects():
                        _options.append(proj.name)

            _optionCleaned = [i for i in _options if i.startswith(text)]

            return _optionCleaned
        except Exception as e:
            self.printer.print_error(e)
            return []
    #endregion

    #region Help Projects
    def help_projects(self) -> None:
        self.printer.help("Create/Delete/Deselect/List/Select/Use project to keep reports orgranized", endingBreaks=0, leadingBreaks=0)
        self.printer.help("Usage : projects [create/delete/deselect/list/select <project_name>]", endingBreaks=0, leadingBreaks=0, leadingText="")
        self.printer.help("Examples", leadingText="")
        self.printer.item_1("projects list")
        self.printer.item_1("projects create test_project", endingBreaks=1)
    #endregion

    #region Do Projects
    def do_projects(self, line: str) -> None:
        try:
            _split = line.split(' ')

            if(_split[0].lower() == "create"):
                if(_split[1].strip() == ""):
                    raise Exception(f'ERROR :: PLEASE SUPPLY A NAME FOR THE PROJECT')
                else:
                    self.projects_db.create_project(Project({"name" : _split[1]}))
                    print("")
            elif(_split[0].lower() == "delete"):
                if(_split[1].strip() == ""):
                    raise Exception(f'ERROR :: PLEASE SUPPLY A PROJECT TO DELETE')
                else:    
                    self.projects_db.delete_project(Project({'name' : _split[1]}))
                    if self.conf.project != None:
                        if self.conf.project.name == _split[1]:
                            self.conf.project = None
            elif(_split[0].lower() == "deselect"):
                self.conf.project = None
                self.printer.print_formatted_check("No Project Set", leadingBreaks=1, endingBreaks=1)
            elif(_split[0].lower() == "list" or _split[0].lower() == ""):
                
                _projects = self.projects_db.list_projects()
                if len(_projects) != 0:
                    self.printer.print_underlined_header("Projects")
                    for proj in _projects:
                        self.printer.item_1(proj.name)
                    print("")
                else:
                    self.printer.print_error(Exception("No Projects"))
            elif(_split[0].lower() == "select"):
                _proj = self.projects_db.select_project(_split[1])
                self.conf.project = _proj
                self.printer.print_formatted_check(f"Selected Project ({_proj.name})", leadingBreaks=1, endingBreaks=1)
            elif(_split[0].lower() == ""):
                self.help_projects()
            else:
                raise Exception(f'ERROR :: ({_split[0]}) :: NOT A VALID COMMAND')
        except Exception as e:
            self.printer.print_error(e)
    #endregion 