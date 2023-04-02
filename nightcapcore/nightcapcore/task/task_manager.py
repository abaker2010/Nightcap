from ..printers import Printer
from .task import Task
from typing import List
from nightcapcore.database.mongo.mongo_tasks import MongoTasksDatabase


class TaskManager(object):

    def __init__(self) -> None:
        self.printer = Printer()
        self._db = MongoTasksDatabase()
        self.tasks:List[Task] = []
        self._loadtasks()
        

    def list(self) -> None:
        print("DB Data")
        print(self._db.read().count())
        print(str(type(self._db.read())))
        self.printer.print_underlined_header("Current Tasks")
        if self.tasks != []:
            for t in self.tasks:
                self.printer.item_1(str(t))
        else:
            self.printer.item_1("No Tasks Available")
    
    def delete(self) -> None:
        self.printer.item_1("Delete Task")
        self._loadtasks()

    def create(self, task_data: dict) -> None:
        self.printer.item_1("Create Task")
        self._db.create(task_data)
        self._loadtasks()

    def _loadtasks(self):
        self.tasks = []
        for t in list(self._db.read()):
            print(t)
            self.tasks.append(Task(**t))
        

    def run(self) -> None:
        self.printer.print_underlined_header("Running Task")
        
        if self.tasks != []:
            for t in self.tasks:
                self.printer.item_1(str(t))
                # t.run()
        else:
            self.printer.item_1("No Tasks Available")
