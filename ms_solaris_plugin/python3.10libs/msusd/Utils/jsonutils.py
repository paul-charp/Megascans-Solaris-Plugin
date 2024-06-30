import json
from ..Logger import Logger


def write_json(d: dict, filepath: str, indent: int = None, logger: Logger = None):
    """
    Writes a dictionary to a JSON file.

    Args:
        d: dict: Specify the dictionary that will be written to a file
        filepath: str: Specify the filepath of the json file to be written
        indent: int: Specify the indentation level of the json file (defaults to None)
        logger: Logger: Log a message using the provided logger if not None (defaults to None)
    """
    with open(filepath, "w+") as json_file:
        json.dump(d, json_file, indent=indent)

    if type(logger) is Logger:
        logger.message(f"Write {filepath}")


def read_json(filepath: str, logger: Logger = None) -> dict:
    """
    Reads a JSON file and returns the data as a dictionary.

    Args:
        filepath: str: Specify the filepath of the json file to be read
        logger: Logger: Log a message using the provided logger if not None (defaults to None)

    Returns:
        A dictionary
    """
    with open(filepath, "r") as json_data:
        d = json.load(json_data)

    if type(logger) is Logger:
        logger.message(f"Read {filepath}")

    return d
