__internal_store__ = {}


def contains_object(key):
    return key in __internal_store__


def set_object(key, value):
    __internal_store__[key] = value


def get_object(key):
    return __internal_store__[key] if contains_object(key) else None


def remove_object(key):
    if contains_object(key):
        del __internal_store__[key]


def clear():
    __internal_store__.clear()
