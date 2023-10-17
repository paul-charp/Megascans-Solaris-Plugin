import datetime
import hou


class Logger:
    __loggers = {}

    source_name = "MSUSD"
    log_file = "$HOUDINI_TEMP_DIR/msusd.log"
    default_console_verbosity = 0
    hou_severity_map = {
        0: hou.severityType.Message,
        1: hou.severityType.ImportantMessage,
        2: hou.severityType.Warning,
        3: hou.severityType.Error,
        4: hou.severityType.Fatal,
    }

    def __init__(self, context):
        if Logger.__loggers.get(context) != None:
            Logger.getLogger(context)

        Logger.__loggers[context] = self

        self.context = context

        self.setConsoleVerbosity(4)

        # if Logger.source_name not in hou.logging.sources():
        hou.logging.createSource(Logger.source_name)

        # if hou.getenv("MSUSD_LOG_FILE") == 1:

        self.message(f"Logger for {self.context} initialized")
        Logger._initFileSink()

    @staticmethod
    def getLogger(context) -> "Logger":
        if Logger.__loggers.get(context) == None:
            Logger(context)
        return Logger.__loggers.get(context)

    def log(self, message, severity=None):
        log_entry = hou.logging.LogEntry(
            message=message,
            source=Logger.source_name,
            source_context=self.context,
            severity=severity,
        )

        hou.logging.log(log_entry, source_name=Logger.source_name)

        if severity != None:
            if severity < self.console_verbosity:
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
        log_file = hou.text.expandString(Logger.log_file)
        file_sink = hou.logging.FileSink(log_file)
        file_sink.connect(Logger.source_name)
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

        print(time, severity, context, message)

    @staticmethod
    def _getDefaultConsoleVerbosity():
        default_console_verbosity = hou.getenv("MSUSD_CONSOLE_VERBOSITY")
        if (
            default_console_verbosity == None
            or default_console_verbosity not in Logger.hou_severity_map.keys()
        ):
            default_console_verbosity = Logger.default_console_verbosity

        return default_console_verbosity

    @staticmethod
    def _getHouSeverity(key):
        return Logger.hou_severity_map[key]

    def setConsoleVerbosity(self, console_verbosity):
        default_verbosity = Logger._getDefaultConsoleVerbosity()

        console_verbosity = min(default_verbosity, console_verbosity)

        hou_severity = Logger._getHouSeverity(console_verbosity)
        self.console_verbosity = hou_severity
