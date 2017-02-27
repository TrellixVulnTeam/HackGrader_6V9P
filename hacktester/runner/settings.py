import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE_DIR, 'input/')
LIBS = os.path.join(BASE_DIR, 'libs/')
JUNIT = os.path.join(LIBS, 'junit.jar')
HAMCREST = os.path.join(LIBS, 'hamcrest.jar')

# Set timelimit in seconds
TIMELIMIT = 3
TIMELIMIT_EXCEEDED_ERROR = 'Time limit exceeded. Maybe infinite loop?'


OUTPUT_CHECKING = "output_checking"
UNITTEST = "unittest"

JAVA = "java"
PYTHON = "python"
RUBY = "ruby"
NODEJS = "nodejs"
