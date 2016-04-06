import os

from .base import BaseGrader, DynamicLanguageExecuteMixin
from .proc import run_cmd
from settings import TIMELIMIT, TIMELIMIT_EXCEEDED_ERROR

from subprocess import (CalledProcessError, TimeoutExpired,
                        Popen, check_output,
                        STDOUT, PIPE)

from .proc import run_cmd, killall


class PythonGrader(DynamicLanguageExecuteMixin, BaseGrader):
    COMMAND = 'python3'
    LANGUAGE_NAME = 'python'


class RubyGrader(DynamicLanguageExecuteMixin, BaseGrader):
    COMMAND = 'ruby'
    LANGUAGE_NAME = 'ruby'
