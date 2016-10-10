import os
import tempfile
import shlex
from subprocess import (CalledProcessError, TimeoutExpired,
                        Popen, call, check_output,
                        STDOUT, PIPE)


def create_input_file(input_string):
    if not input_string:
        input_string = ""

    input_file = tempfile.NamedTemporaryFile()
    input_file.write(input_string.encode('utf-8'))
    input_file.seek(0)
    return input_file


def run_cmd(cmd, timeout, input_string=None):
    args = shlex.split(cmd)
    output = tempfile.NamedTemporaryFile()
    input_file = create_input_file(input_string)

    proc = Popen(args,
                 stdout=output,
                 stderr=output,
                 stdin=input_file,
                 universal_newlines=True,
                 bufsize=0)

    try:
        proc.communicate(timeout=timeout)
        returncode = proc.returncode
    except TimeoutExpired:
        proc.kill()
        raise
    finally:
        with open(output.name, 'r') as f:
            output = f.read()

    return returncode, output


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
