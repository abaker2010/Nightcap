
# region Imports
import enum
import os

# endregion


class NightcapPathsEnum(enum.Enum):
    """

    This class is used as an enum for where to generate the package paths

    ...

    Attributes
    ----------
        ProjectBase
        Reporting
        ReportingTemplates

    """

    ProjectBase = os.sep.join(["nightcore", "nightcore"])
    Reporting = "reporting"
    ReportingTemplates = os.sep.join(["server", "webbase"])
