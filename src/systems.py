from pathlib2 import Path
import os
from subprocess import Popen, PIPE, STDOUT
from psutil import AccessDenied, Process, TimeoutExpired

from .logs import *
from .utils import DEVNULL

def _kill_process(proc):
    """Tries to kill the process otherwise just logs a debug message, the
    process will be killed when thefuck terminates.

    :type proc: Process

    """
    try:
        proc.kill()
    except AccessDenied:
        info_print(
            "Rerun: process PID {} ({}) could not be terminated".format(
                proc.pid, proc.exe()
            )
        )


def _wait_output(popen):
    """Returns `True` if we can get output of the command in the
    `settings.wait_command` time.

    Command will be killed if it wasn't finished in the time.

    :type popen: Popen
    :rtype: bool

    """
    proc = Process(popen.pid)
    try:
        proc.wait(2)
        return True
    except TimeoutExpired:
        for child in proc.children(recursive=True):
            _kill_process(child)
        _kill_process(proc)
        return False


def run_command(command):
    result = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    if _wait_output(result):
        output = result.stdout.read().decode('utf-8', errors='replace')
        return output
    else:
        info_print(u'Execution timed out!')
        return None

def _expanduser(self):
    return self.__class__(os.path.expanduser(str(self)))


if not hasattr(Path, "expanduser"):
    Path.expanduser = _expanduser


if __name__=="__main__":
    command = "echo hello; sleep 1; echo world "
    os.system(command)