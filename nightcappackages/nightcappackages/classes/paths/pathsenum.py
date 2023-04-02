# region Imports
import enum
import os
# endregion

class NightcapPackagesPathsEnum(enum.Enum):
    ProjectBase = "classes"
    PackagesBase = "packages"
    Installers = "installers"
    NCInitRestore = "init_restore_point"
    Databases = ProjectBase + os.sep + "databases"
