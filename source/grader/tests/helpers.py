import sys
import os
from subprocess import check_output, STDOUT
import json

sys.path.append('../')
from settings import INPUT

DATA_FILE = os.path.join(INPUT, 'data.json')


def call_start():
    return check_output(['python3', 'start.py'], stderr=STDOUT).decode('utf-8')


def save_data_json(data):
    with open(DATA_FILE, 'w') as f:
        f.write(json.dumps(data))


def save_file(name, code):
    path = os.path.join(INPUT, name)

    with open(path, 'w') as f:
        f.write(code)
