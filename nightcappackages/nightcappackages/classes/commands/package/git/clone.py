# region Imports
import git
from nightcapcore.command.command import Command
from nightcapcore import Printer

# endregion

class NightcapPackageGitCloneCommand(Command):
    # region Init
    def __init__(
        self,
        url: str,
        tmppath: str,
        commit_id: str = None,
        verbose: bool = False,
    ):
        self.printer = Printer()
        self.verbose = verbose
        self.url = url
        self.tmppath = tmppath
        self.commit_id = commit_id
        # self.git = None

    def execute(self) -> None:

        try:
            if self.commit_id != None:
                self.printer.print_formatted_additional("Trying to use commit id :: %s" % (self.commit_id))
                repo = git.Repo.clone_from(self.url, self.tmppath, no_checkout=True)
                repo.git.checkout(self.commit_id)
            else:
                git.Repo.clone_from(self.url, self.tmppath)
            return True
        except Exception as e:
            self.printer.print_error(e)
            raise e
    # endregion