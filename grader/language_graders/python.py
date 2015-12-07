from .base import BaseGrader


class PythonGrader(BaseGrader):
    COMMAND = 'python3'
    ARGS = '{tests}'
