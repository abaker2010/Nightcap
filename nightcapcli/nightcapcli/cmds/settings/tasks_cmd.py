# region Imports
from typing import List
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcore import TaskManager, Task
# endregion


class NightcapTasksCMD(NightcapBaseCMD):
    # region Init
    def __init__(self, channelID: str = None) -> None:
        NightcapBaseCMD.__init__(self, ["settings", "tasks"], channelid=channelID)
        self.task_manager = TaskManager()
    
    # endregion

    def help_test(self) -> None:
        self.printer.help("Testing Task")

    def do_test(self, line) -> None:
        self.task_manager.run()

    def help_create(self) -> None:
        self.printer.help("Building a task")
    
    def do_create(self, line) -> None:
        _task = {}

        _name = self.printer.input_return_only("Task Name")
        _task['name'] = _name
        
        _packages = []
        while self.printer.input("Add package to task: [Y/n]", defaultReturn=True):
            _packages.append(self._add_package())

        _task['packages'] = _packages

        self.task_manager.create(_task)

    def _add_package(self) -> dict:
        
        return {"test" : "package data"}


    def help_list(self) -> None:
        self.printer.help("List current tasks")
    
    def do_list(self, line) -> None:
        self.task_manager.list()

    def help_delete(self) -> None:
        self.printer.help("Delete a task")
    
    def do_delete(self, line) -> None:
        self.task_manager.delete()

