import os


def get_directory():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    return dirpath
