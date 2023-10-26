import os
import hou
from .Utils import dictutils, jsonutils
from .Logger import Logger


class SettingsManager:
    """
    Settings Manager class.
        Use SettingsManager.getInstance() to get or create the settings manager.
        The Settings Manager hold the settings loaded from the settings file.
        It guarantees that all the keys of the default settings are present in the provided settings as well a the values types.
        Default settings and settings file location are defined in this class.
    """

    __instance = None

    defaultSettings = {
        "socket_port": 24981,
        "export_paths": ["$HIP/usd", "$MSLIB/usd"],
        "export_settings": {},
    }

    settingsFile = "$HOUDINI_USER_PREF_DIR/msusd_settings.json"

    def __init__(self):
        """
        Sets up the instance of SettingsManager, and loads settings from a file if it exists.
            If no settings file exists, it creates one with default values.
            if the settings file exists but its settings are not validated,
                it loads the default settings without changing the settings file

        Args:
            self: Represent the instance of the class
        """
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
        """
        Static method that returns the singleton instance of the SettingsManager class.
            If no instance exists, it creates one and then returns it.

        Returns:
            An instance of the settingsmanager class
        """
        if SettingsManager.__instance == None:
            SettingsManager()
        return SettingsManager.__instance

    @staticmethod
    def _getJsonSettings():
        """
        Private function that reads the settings file and returns it as a dictionary.
            If the settings file does not exist, then None is returned.

        Returns:
            A dictionary
        """
        settingsFile = hou.text.expandString(SettingsManager.settingsFile)

        if not os.path.isfile(settingsFile):
            return None

        json_data = jsonutils.read_json(settingsFile)
        return json_data

    @staticmethod
    def validateSettings(settings, defaultSettings=defaultSettings) -> tuple:
        """
        Takes a settings dictionary and validates it against the defaultSettings.
            Checks keys presence and value types.

        Args:
            settings: the settings to validate
            defaultSettings: the settings to validated against

        Returns:
            A tuple of (bool, error)
        """
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
        """
        Takes a dictionary of settings and merges it with the current settings.
            The new values will overwrite any existing ones.

        Args:
            self: Represent the instance of the class
            settings: dict: the settings to replace/merge
        """
        result, error = dictutils.validateDict(settings)

        if not result:
            raise error

        merged = dictutils.merge([settings, self.getSettings()])
        self.__settings = merged

    def putSetting(self, key: str, value):
        """
        Set a value in the settings dictionary.
            The key parameter is the name of the setting, and value is its new value.
            If there are any sub-dictionaries in between, they will be created if necessary.

        Args:
            self: Represent the instance of the class
            key: str: Set the key of the setting (navigate nested dicts with "." between keys)
            value: Set the value of a key in the settings dictionary
        """
        dictutils.setValue(self.__settings, key, value)

    def saveSettings(self):
        """
        Saves the settings to the json file.
            The function takes no arguments and returns nothing.

        Args:
            self: Represent the instance of the class
        """
        settingsFile = hou.text.expandString(SettingsManager.settingsFile)

        jsonutils.write_json(self.getSettings(), settingsFile, indent=4)

        self.logger.message("Settings Saved")

    def getSettings(self, key=None):
        """
            If a key is provided, it will return the value of that key in the settings dictionary.
                If not, it will return the complete settings dictionary.

        Args:
            self: Represent the instance of the class
            key: Get a specific value from the settings dictionary

        Returns:
            The value of the key parameter or the settings dictionary
        """
        if key != None:
            return dictutils.getValue(self.__settings, key)
        return self.__settings
