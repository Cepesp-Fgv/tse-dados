def opt(dictionary, key, default=None):
    return dictionary[key] if key in dictionary else default


def arg(dictionary, key):
    if key not in dictionary:
        raise KeyError(f'No argument {key} supplied')

    return dictionary[key]
