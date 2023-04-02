import sys
import subprocess
from typing import List, Tuple

class CustomSubprocess(object):
    def __init__(self, arguments: List[str] = None):
        self.args = arguments

    def execute(self) -> Tuple[int, List[str]]:
        try:
            process = subprocess.Popen(self.args, 
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        bufsize=0,
                                        universal_newlines=True
                                    )
            return_data = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    return_data.append(output)
                    sys.stdout.write("\t" + output)
                    sys.stdout.flush()
                    process.stdout.flush()
            rc = process.poll()
            return (rc, return_data)
        except Exception as e:
            raise e