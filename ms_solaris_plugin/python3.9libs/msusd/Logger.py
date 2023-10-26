import datetime
import hou


class Logger:
    """
    Logger class.
        Overall just a big wrapper around the hou.logging module functionalities.
        Manage multiples source context in the source "MSUSD" (Logger.SOURCE_NAME)
        Sends all logs to the file defined in Logger.LOG_FILE
        Sends logs to console if a log severity is higher that the matching console verbosity set for the context.
        Use Logger.getLogger() to get and create instances of this class.
    """

    __loggers = {}

    fileSink = None
    SOURCE_NAME = "MSUSD"
    LOG_FILE = "$HOUDINI_TEMP_DIR/msusd.log"
    DEFAULT_CONSOLE_VERBOSITY = 2
    HOU_SEVERITY_MAP = [
        hou.severityType.Fatal,
        hou.severityType.Error,
        hou.severityType.Warning,
        hou.severityType.ImportantMessage,
        hou.severityType.Message,
    ]

    def __init__(self, context: str):
        """
        It sets up the logger for a given context, and initializes it with a default verbosity of 0.
        If there's already an existing logger for that context, it returns that one instead.

        Args:
            context: str: Identify the loggers
        """
        if Logger.__loggers.get(context) != None:
            Logger.getLogger(context)

        Logger.__loggers[context] = self

        self.context = context

        self.setConsoleVerbosity(0)

        if Logger.SOURCE_NAME not in hou.logging.sources():
            hou.logging.createSource(Logger.SOURCE_NAME)

            if hou.getenv("MSUSD_LOG_FILE") == "1":
                if Logger.fileSink == None:
                    Logger.fileSink = Logger._initFileSink()

        self.message(f"Logger for {self.context} initialized")

    @staticmethod
    def getLogger(context: str) -> "Logger":
        """
        Factory function that returns a Logger object.
            If the logger has not been created yet.
            Otherwise, it will return an existing logger.

        Args:
            context: str: Create a new logger object with the context as its name

        Returns:
            A logger object
        """
        if Logger.__loggers.get(context) == None:
            Logger(context)
        return Logger.__loggers.get(context)

    @staticmethod
    def _initFileSink() -> hou.logging.FileSink:
        """
        The _initFileSink function is a private function that initializes the file sink.
            The file sink is used to write log messages to a text file.
            It takes no arguments and returns an instance of hou.logging.FileSink.

        Returns:
            A file sink
        """
        log_file = hou.text.expandString(Logger.LOG_FILE)
        file_sink = hou.logging.FileSink(log_file)
        file_sink.connect(Logger.SOURCE_NAME)
        return file_sink

    @staticmethod
    def _logToConsole(log_entry: hou.logging.LogEntry) -> str:
        """
        Returns and prints to the console a string representation of the hou.logging.LogEntry object.

        Args:
            log_entry: hou.logging.LogEntry: Pass the log entry to the function

        Returns:
            A string
        """
        message = log_entry.message()
        time = log_entry.time()
        context = log_entry.sourceContext()
        severity = log_entry.severity()

        dt_object = datetime.datetime.fromtimestamp(time)
        time = dt_object.strftime("%H:%M:%S.%f")[:-3]

        severity = str(severity).split(".")[-1].upper()

        print_str = f"{time} {severity} {context} - {message}"
        print(print_str)
        return print_str

    @staticmethod
    def _getDefaultConsoleVerbosity() -> int:
        """
        Private function that returns the default console verbosity.
            The default console verbosity is determined by the MSUSD_CONSOLE_VERBOSITY environment variable,
            which can be set to any of the following values:
                0 - Fatal (less verbose)
                1 - Error
                2 - Warning (default)
                3 - ImportantMessage
                4 - Message (most verbose)

            If the variable is not set or is not an integer the verbosity defaults to 2 - Warning :
                (see constant : Logger.DEFAULT_CONSOLE_VERBOSITY)

        Returns:
            An integer
        """
        default_console_verbosity = hou.getenv("MSUSD_CONSOLE_VERBOSITY")
        default_console_verbosity = int(default_console_verbosity)
        try:
            default_console_verbosity = Logger._clampVerbosityIndex(
                int(default_console_verbosity)
            )
            Logger._getHouSeverity(default_console_verbosity)

        except (IndexError, TypeError, ValueError) as e:
            default_console_verbosity = Logger.DEFAULT_CONSOLE_VERBOSITY

        return default_console_verbosity

    @staticmethod
    def _clampVerbosityIndex(index: int) -> int:
        """
        Helper function that takes an integer index and returns the closest valid
        index to it.  The valid indices are 0, 1, 2, 3, 4.  (Defined by the length of the Logger.HOU_SEVERITY_MAP array.)

        Args:
            index: int: Index to clamp

        Returns:
            Clamped Index
        """
        return sorted((0, index, len(Logger.HOU_SEVERITY_MAP) - 1))[1]

    @staticmethod
    def _getHouSeverity(key: int) -> hou.EnumValue:
        """
        Helper function that takes in an integer and returns the corresponding hou.EnumValue object from the Logger.HOU_SEVERITY_MAP dictionary.

        Args:
            key: int: Severity index

        Returns:
            The hou.severityType enum value corresponding to the index.
        """
        return Logger.HOU_SEVERITY_MAP[key]

    def log(self, message, severity: hou.EnumValue = None) -> hou.logging.LogEntry:
        """
        Wrapper around the hou.logging.log function, which allows for logging to the Houdini console and log file.

        Args:
            message: str or Exception: Pass the message to be logged (can be a string or a Exception object that will be converted to a string)
            severity: hou.SeverityType enum value: Determine the severity of the message (defaults to None)

        Returns:
            A hou.logging.LogEntry object
        """
        if type(message) != str:
            message = str(message)

        log_entry = hou.logging.LogEntry(
            message=message,
            source=Logger.SOURCE_NAME,
            source_context=self.context,
            severity=severity,
        )

        hou.logging.log(log_entry, source_name=Logger.SOURCE_NAME)

        if severity != None:
            verbosity = Logger.HOU_SEVERITY_MAP.index(severity)
            if verbosity <= self.console_verbosity:
                Logger._logToConsole(log_entry)

        return log_entry

    def fatal(self, message) -> hou.logging.LogEntry:
        """
        Log a message with the severity of Fatal.
            Wrapper around the log() method.

        Args:
            message: message to log

        Returns:
            A logentry object
        """
        return self.log(message, severity=hou.severityType.Fatal)

    def error(self, message) -> hou.logging.LogEntry:
        """
        Log a message with the severity of Error.
            Wrapper around the log() method.

        Args:
            message: message to log

        Returns:
            A logentry object
        """
        return self.log(message, severity=hou.severityType.Error)

    def warning(self, message) -> hou.logging.LogEntry:
        """
        Log a message with the severity of Warning.
            Wrapper around the log() method.

        Args:
            message: message to log

        Returns:
            A logentry object
        """
        return self.log(message, severity=hou.severityType.Warning)

    def importantMessage(self, message) -> hou.logging.LogEntry:
        """
        Log a message with the severity of ImportantMessage.
            Wrapper around the log() method.

        Args:
            message: message to log

        Returns:
            A logentry object
        """
        return self.log(message, severity=hou.severityType.ImportantMessage)

    def message(self, message) -> hou.logging.LogEntry:
        """
        Log a message with the severity of Message.
            Wrapper around the log() method.

        Args:
            message: message to log

        Returns:
            A logentry object
        """
        return self.log(message, severity=hou.severityType.Message)

    def setConsoleVerbosity(self, console_verbosity: int, force=False):
        """
        Sets the console verbosity of a Logger object.

        Args:
            console_verbosity: int: Set the verbosity level of the console
            force: Force the verbosity level to be set even if it is lower than the default console verbosity
        """
        if not force:
            default_verbosity = Logger._getDefaultConsoleVerbosity()
            console_verbosity = max(default_verbosity, console_verbosity)

        self.console_verbosity = Logger._clampVerbosityIndex(console_verbosity)
