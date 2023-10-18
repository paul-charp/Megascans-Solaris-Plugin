import json
from ..Logger import Logger


def write_json(d: dict, filepath: str, indent=None, logger=None):
    with open(filepath, "w+") as json_file:
        json.dump(d, json_file, indent=indent)

    if type(logger) is Logger:
        logger.message(f"Write {filepath}")


def read_json(filepath: str, logger=None) -> dict:
    with open(filepath, "r") as json_data:
        d = json.load(json_data)

    if type(logger) is Logger:
        logger.message(f"Read {filepath}")

    return d
