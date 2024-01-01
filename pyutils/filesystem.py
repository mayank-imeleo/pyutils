import pathlib


def mkdir(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
