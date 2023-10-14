PATH_SEPARATOR = "."


def validateKey(key: str):
    if type(key) != str:
        return (False, TypeError(f"Key {key} is not a string"))

    if PATH_SEPARATOR in key:
        return (False, Exception(f"Key {key} contain {PATH_SEPARATOR}"))

    return (True, None)


def validateDict(obj: dict):
    for key, value in obj.items():
        result, error = validateKey(key)
        if not result:
            return (False, error)

        if type(value) is dict:
            result, error = validateDict(value)
            if not result:
                return (False, error)

    return (True, None)


def getValue(obj: dict, path: str):
    result, error = validateDict(obj)
    if not result:
        raise error

    keys = path.split(PATH_SEPARATOR)

    root = obj
    for key in keys:
        try:
            root = root[key]
        except Exception:
            raise KeyError(f"{path} -> '{key}' is not a valid key")

    return root


def setValue(obj: dict, path: str, value):
    result, error = validateDict(obj)
    if not result:
        raise error

    keys = path.split(PATH_SEPARATOR)
    lkey = len(keys) - 1
    root = obj
    for index, key in enumerate(keys):
        try:
            if index == lkey:
                root[key] = value
                return

            root = root[key]
        except:
            root[key] = {}
            root = root[key]


def merge(dicts: list[dict]):
    result = {}
    for d in dicts:
        for key, value in d.items():
            if key not in result:
                result[key] = value
            else:
                if isinstance(result[key], list) and isinstance(value, list):
                    result[key].extend(value)
                elif isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge([result[key], value])
    return result
