import os
import tempfile
import shlex
from subprocess import (CalledProcessError, TimeoutExpired,
                        Popen, call, check_output,
                        STDOUT, PIPE)


def run_cmd(cmd, timeout):
    args = shlex.split(cmd)
    output = tempfile.NamedTemporaryFile()

    proc = Popen(args,
                 stdout=output,
                 stderr=output,
                 universal_newlines=True,
                 bufsize=0)

    try:
        proc.communicate(timeout=timeout)
        returncode = proc.returncode
    except TimeoutExpired:
        proc.kill()
        returncode = 137
    finally:
        with open(output.name, 'r') as f:
            output = f.read()

    return (returncode, output)


def kill(pid):
    cmd = 'kill {}'.format(pid)
    args = shlex.split(cmd)

    call(args)


def killall(proc):
    cmd = 'pgrep {}'.format(proc)
    args = shlex.split(cmd)

    try:
        output = check_output(args).decode('utf-8').split('\n')
        current_pid = os.getpid()

        pids = [int(pid) for pid in output if pid != "" and int(pid) != current_pid]

        for pid in pids:
            kill(pid)
    except CalledProcessError:
        pass
