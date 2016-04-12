import base64


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def read_binary_file(path):
    """Returns the file in base64 encoding"""

    with open(path, 'rb') as f:
        encoded = base64.b64encode(f.read())

    return encoded.decode('ascii')
