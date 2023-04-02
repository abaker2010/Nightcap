

# region Imports
import enum
# endregion

class NightcapDockerStatus(enum.Enum):
    """
    This class is used as an enum for where to generate the docker status
    ...

    """

    STOPPED = "stopped"
    RUNNING = "running"
    MISSING = "missing"
    STARTED = "started"
    PAUSED = "paused"
    EXISTS = "exists"
    MANDITORY = "manditory"
    NOTMANDITORY = "not manditory"
    PASSING = "passing"
    FAILED = "failed"
