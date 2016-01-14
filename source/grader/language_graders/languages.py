from .base import BaseGrader


class PythonGrader(BaseGrader):
    LANGUAGE_NAME = 'python'
    COMMAND = 'python3'
    ARGS = '{tests}'


class RubyGrader(BaseGrader):
    LANGUAGE_NAME = 'ruby'
    COMMAND = 'ruby'
    ARGS = '{tests}'
