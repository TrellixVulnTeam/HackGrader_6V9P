import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE_DIR, 'input/')
LIBS = os.path.join(BASE_DIR, 'libs/')
JUNIT = os.path.join(LIBS, 'junit.jar')
HAMCREST = os.path.join(LIBS, 'hamcrest.jar')

# Set timelimit in seconds
TIMELIMIT = 3
TIMELIMIT_EXCEEDED_ERROR = 'Time limit exceeded. Maybe infinite loop?'

# test types
OUTPUT_CHECKING = "output_checking"
UNITTEST = "unittest"

# languages
JAVA = "java"
PYTHON = "python"
RUBY = "ruby"
JAVASCRIPT = "javascript/nodejs"

# dependencies filenames and timelimits
DEPENDENCIES_TIMELIMIT = 300
DJANGO_DEPENDENCIES_FILENAME = "requirements.txt"

PYTHON_VIRTUALENV_ACTIVATION_PATH = "/virtualenvs/current/bin/activate"
