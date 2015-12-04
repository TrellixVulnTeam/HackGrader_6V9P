from .base import BaseGrader


class PythonGrader(BaseGrader):
    SOLUTION_FILE = 'solution.py'
    TESTS_FILE = 'tests.py'
    COMMAND = 'python3'
    ARGS = '{tests}'
