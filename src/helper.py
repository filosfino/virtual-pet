import uos


def file_exists(path):
    try:
        uos.stat(path)
        return True
    except OSError:
        return False


def is_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True
