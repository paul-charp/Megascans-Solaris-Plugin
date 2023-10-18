import datetime
import hou


class Logger:
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

    def __init__(self, context):
        if Logger.__loggers.get(context) != None:
            Logger.getLogger(context)

        Logger.__loggers[context] = self

        self.context = context

        self.setConsoleVerbosity(0)

        if Logger.SOURCE_NAME not in hou.logging.sources():
            print("createSource")
            hou.logging.createSource(Logger.SOURCE_NAME)

            if hou.getenv("MSUSD_LOG_FILE") == "1":
                if Logger.fileSink == None:
                    Logger.fileSink = Logger._initFileSink()

        self.message(f"Logger for {self.context} initialized")

    @staticmethod
    def getLogger(context) -> "Logger":
        if Logger.__loggers.get(context) == None:
            Logger(context)
        return Logger.__loggers.get(context)

    def log(self, message, severity=None):
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

    def fatal(self, message):
        return self.log(message, severity=hou.severityType.Fatal)

    def error(self, message):
        return self.log(message, severity=hou.severityType.Error)

    def warning(self, message):
        return self.log(message, severity=hou.severityType.Warning)

    def importantMessage(self, message):
        return self.log(message, severity=hou.severityType.ImportantMessage)

    def message(self, message):
        return self.log(message, severity=hou.severityType.Message)

    @staticmethod
    def _initFileSink():
        log_file = hou.text.expandString(Logger.LOG_FILE)
        file_sink = hou.logging.FileSink(log_file)
        file_sink.connect(Logger.SOURCE_NAME)
        return file_sink

    @staticmethod
    def _logToConsole(log_entry):
        message = log_entry.message()
        time = log_entry.time()
        context = log_entry.sourceContext()
        severity = log_entry.severity()

        dt_object = datetime.datetime.fromtimestamp(time)
        time = dt_object.strftime("%H:%M:%S.%f")[:-3]

        severity = str(severity).split(".")[-1].upper()

        print_str = f"{time} {severity} {context} - {message}"

        print(print_str)

    @staticmethod
    def _getDefaultConsoleVerbosity():
        default_console_verbosity = hou.getenv("MSUSD_CONSOLE_VERBOSITY")

        try:
            Logger._getHouSeverity(default_console_verbosity)

        except (IndexError, TypeError):
            default_console_verbosity = Logger.DEFAULT_CONSOLE_VERBOSITY

        return default_console_verbosity

    @staticmethod
    def _getHouSeverity(key):
        return Logger.HOU_SEVERITY_MAP[key]

    def setConsoleVerbosity(self, console_verbosity, force=False):
        if force:
            self.console_verbosity = console_verbosity

        else:
            default_verbosity = Logger._getDefaultConsoleVerbosity()
            self.console_verbosity = max(default_verbosity, console_verbosity)
