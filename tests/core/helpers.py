import os

TESTS_PATH = os.path.abspath(os.path.dirname(__file__) + os.path.sep + '..')


def read(path, mode='rb'):
    if not os.path.isabs(path):
        path = os.path.join(TESTS_PATH, path)

    path = os.path.abspath(path)

    with open(path, mode) as fp:
        return fp.read()
