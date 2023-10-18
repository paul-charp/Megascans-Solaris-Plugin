import os
import hou
import json
from .Utils import dictutils
from .Logger import Logger


class SettingsManager:
    __instance = None

    defaultSettings = {
        "socket_port": 24981,
        "export_paths": ["$HIP/usd", "$MSLIB/usd"],
        "export_settings": {},
    }

    settingsFile = "$HOUDINI_USER_PREF_DIR/msusd_settings.json"

    def __init__(self):
        if SettingsManager.__instance != None:
            SettingsManager.getInstance()

        SettingsManager.__instance = self

        self.logger = Logger.getLogger("SettingsManager")

        self.__settings = {}

        jsonSettings = SettingsManager._getJsonSettings()
        if jsonSettings != None:
            result, error = SettingsManager.validateSettings(jsonSettings)
            if result:
                self.putSettings(jsonSettings)

            else:
                self.logger.warning(error)
                self.putSettings(SettingsManager.defaultSettings)
        else:
            self.logger.importantMessage(
                "Settings file not found, creating default settings"
            )
            self.putSettings(SettingsManager.defaultSettings)
            self.saveSettings()

        self.logger.message("Settings Initialized")

    @staticmethod
    def getInstance():
        if SettingsManager.__instance == None:
            SettingsManager()
        return SettingsManager.__instance

    @staticmethod
    def _getJsonSettings():
        settingsFile = hou.text.expandString(SettingsManager.settingsFile)

        if not os.path.isfile(settingsFile):
            return None

        with open(settingsFile, "r") as settingsJson:
            json_data = json.load(settingsJson)

        return json_data

    @staticmethod
    def validateSettings(settings, defaultSettings=defaultSettings):
        result, error = dictutils.validateDict(settings)

        if not result:
            return (False, error)

        for key, defaultValue in defaultSettings.items():
            if key not in settings:
                return (False, KeyError(f"Settings {key} is missing"))

            if type(settings[key]) is dict and type(defaultValue) is dict:
                result, error = SettingsManager.validateSettings(
                    settings[key], defaultSettings=defaultValue
                )
                if not result:
                    return (False, error)

            elif type(settings[key]) != type(defaultValue):
                return (
                    False,
                    TypeError(f"Setting {key} not of type {type(defaultValue)}"),
                )

        return (True, None)

    def putSettings(self, settings: dict):
        result, error = dictutils.validateDict(settings)

        if not result:
            raise error

        merged = dictutils.merge([settings, self.getSettings()])
        self.__settings = merged

    def putSetting(self, key: str, value):
        dictutils.setValue(self.__settings, key, value)

    def saveSettings(self):
        settingsFile = hou.text.expandString(SettingsManager.settingsFile)

        with open(settingsFile, "w+") as settingsJson:
            json.dump(self.getSettings(), settingsJson, indent=4)

        self.logger.message("Settings Saved")

    def getSettings(self, key=None):
        if key != None:
            return dictutils.getValue(self.__settings, key)
        return self.__settings
