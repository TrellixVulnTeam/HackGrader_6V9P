import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE_DIR, 'input/')
LIBS = os.path.join(BASE_DIR, 'libs/')
JUNIT = os.path.join(LIBS, 'junit.jar')
HAMCREST = os.path.join(LIBS, 'hamcrest.jar')

# Set timelimit in seconds
TIMELIMIT = 20
TIMELIMIT_EXCEEDED_ERROR = 'Time limit exceeded. Maybe infinite loop?'

# test types
OUTPUT_CHECKING = "output_checking"
UNITTEST = "unittest"

# solution and test file/dir name
SOLUTION_NAME = "solution"
TEST_NAME = "test"

# languages
JAVA = "java"
PYTHON = "python"
RUBY = "ruby"
JAVASCRIPT = "javascript/nodejs"

# dependencies timelimit
DEPENDENCIES_TIMELIMIT = 60
