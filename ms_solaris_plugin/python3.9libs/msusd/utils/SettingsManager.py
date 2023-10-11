from logging.handlers import DEFAULT_UDP_LOGGING_PORT
import hou
import json
from .misc import merge_dicts_recursive

SETTINGS_FILE_NAME = "msusd_settings.json"
SETTINGS_DEFAULT_PATH = f"$HOUDINI_USER_PREF_DIR/{SETTINGS_FILE_NAME}"

DEFAULT_SETTINGS = {
    "socket_port": 24981,
    "export_paths": ["$HIP/usd", "$MSLIB/usd"],
    "export_settings": {},
}


def getJsonSettings():
    try:
        files = hou.findFiles(SETTINGS_FILE_NAME)
        settings_data = []

        for file in files:
            with open(file, "r") as json_file:
                json_data = json.load(json_file)
            settings_data.append(json_data)

        settings = merge_dicts_recursive(settings_data)
        return settings

    except hou.OperationFailed:
        return None

    except Exception as e:
        raise (e)


def saveSettings(settings):
    if getJsonSettings() != None:
        settings_list = [getJsonSettings(), settings]

    else:
        settings_list = [settings]

    updated_settings = merge_dicts_recursive(settings_list)
    settings_path = hou.text.expandString(SETTINGS_DEFAULT_PATH)

    with open(settings_path, "w+") as json_file:
        json.dump(updated_settings, json_file, indent=4)

    return updated_settings


def initSettings():
    if getJsonSettings() == None:
        settings = saveSettings(DEFAULT_SETTINGS)

    else:
        settings = getJsonSettings()

    return settings
