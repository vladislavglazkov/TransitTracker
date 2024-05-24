map = {}


def handles_status(f):
    map[f.__name__] = f
    return f


def get_handler(status: str):
    if status in map:
        return map[status]
    return None
