import os


def fixture(name):
    filename = os.path.join(os.path.dirname(__file__), 'fixtures', name)
    with open(filename, 'r') as f:
        return f.read()


class RequestMock(object):
    env = {}