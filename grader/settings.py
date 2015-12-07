import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE_DIR, 'input/')

# Set timelimit in seconds
TIMELIMIT = 2
TIMELIMIT_EXCEEDED_ERROR = 'Time limit exceeded. Maybe infinite loop?'
