"""
Module providing function to work with dictionary and nested dictionaries
"""

PATH_SEPARATOR = "."


def validateKey(key: str):
    """
    Takes a key as an argument and returns a tuple of two values:
        1. A boolean indicating whether the key is valid or not
        2. An error object if the key is invalid, otherwise None

        A key is valid if it's a string and it doesn't contains the path separator.

    Args:
        key: str: the key

    Returns:
        A tuple(bool, Exception)
    """
    if type(key) != str:
        return (False, TypeError(f"Key {key} is not a string"))

    if PATH_SEPARATOR in key:
        return (False, Exception(f"Key {key} contain {PATH_SEPARATOR}"))

    return (True, None)


def validateDict(obj: dict):
    """
    Takes a dictionary as an argument and recursively validates the keys of each nested dictionary.
        If any key is invalid, it returns False and the error message. Otherwise, it returns True.
        A key is valid if it's a string and it doesn't contains the path separator.

    Args:
        obj: dict: the dictionary to validate

    Returns:
        A tuple(bool, Exception)
    """
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
    """
    Takes a dictionary and a path string as input.
        The path string is expected to be in the format of 'key_name' or 'key_name.sub_key'.
        If the key does not exist, an exception will be raised.

    Args:
        obj: dict: the dictionary to get the value from
        path: str: Specify the path to the value in question

    Returns:
        The value of at given path
    """
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
    """
    Takes a dictionary, a path string and a value.
        The path string is used to traverse the dictionary and set the value at that location.
        The path string is expected to be in the format of 'key_name' or 'key_name.sub_key'.
        If any of the keys in the path do not exist, they are created as empty dictionaries.

    Args:
        obj: dict: Specify the dictionary to be modified
        path: str: Specify the path to the value you want to set
        value: Value to set at the last key in path
    """
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
    """
    Takes a list of dictionaries and merges them into one dictionary recursively.
        If the same key is present in multiple dictionaries, then the value for that key will the value of the first dictionary in the list.
        If any of those values are themselves lists, they will be merged.

    Args:
        dicts: list[dict]: Pass a list of dictionaries to the function

    Returns:
        A dict with all the keys from all the input dicts
    """
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
