import base64
import tarfile
import os


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def read_binary_file(path):
    """Returns the file in base64 encoding"""

    with open(path, 'rb') as f:
        encoded = base64.b64encode(f.read())

    return encoded.decode('ascii')


def create_tar_gz_archive(language):
    path_to_tests = os.path.join("fixtures", "output_check", language, "tests")
    test_files = (file for file in os.listdir(path_to_tests) if os.path.isfile(file))
    with tarfile.open(name="archive.tar.gz", mode="w:gz") as tar:
        for file in test_files:
            path_to_file = os.path.join(path_to_tests, file)
            tar.add(path_to_file)

    return tar.name


def output_checking_test_binary(language):
    test_archive = create_tar_gz_archive(language)
    binary = read_binary_file(test_archive)
    os.remove(test_archive)

    return binary
