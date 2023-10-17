import datetime
import hou

class Logger(): 
    __loggers = {}
    
    source_name = 'MSUSD'
    log_file = "$HOUDINI_TEMP_DIR/msusd.log"
    default_console_verbosity = 3
    console_verbosity_map = {
        0: hou.severityType.Message,
        1: hou.severityType.ImportantMessage,
        2: hou.severityType.Warning,
        3: hou.severityType.Error,
        4: hou.severityType.Fatal
    }
    
    def __init__(self, context, console_verbosity=hou.severityType.Message):     
        if Logger.__loggers.get(context) != None:
            Logger.getLogger(context)

        Logger.__loggers[context] = self
         
        self.context = context
        
        console_verbosity_settings = hou.getenv('MSUSD_CONSOLE_VERBOSITY')
        if console_verbosity_settings == None and console_verbosity_settings not in console_verbosity_map.keys():
            console_verbosity_settings = Logger.default_console_verbosity

            
        hou_console_verbosity_settings = console_verbosity_map[console_verbosity_settings]
        self.console_verbosity = min(hou_console_verbosity_settings, console_verbosity)   
        
        if Logger.source_name not in hou.logging.sources():
            hou.logging.createSource(Logger.source_name)
            
            if hou.getenv('MSUSD_LOG_FILE'):
                Logger._initFileSink()
                

    @staticmethod
    def getLogger(context):
        if Logger.__loggers.get(context) == None:
            Logger(context)
        return Logger.__loggers.get(context)
    


    def log(self, message, severity=None):
        

        
        log_entry = hou.logging.LogEntry(message=message,
                                         source_name=Logger.source_name,
                                         source_context=self.context,
                                         severity=severity)
        
        hou.logging.log(log_entry)
        
        if severity != None:
            if severity < self.console_verbosity:
                Logger._logToConsole(log_entry)
        
        return log_entry
    
    
    def fatal(self, message):
        return self.log(self, message, severity=hou.severityType.Fatal)
    
    def error(self, message):
        return self.log(self, message, severity=hou.severityType.Error)
    
    def warning(self, message):
        return self.log(self, message, severity=hou.severityType.Warning)
    
    def importantMessage(self, message):
        return self.log(self, message, severity=hou.severityType.ImportantMessage)
    
    def message(self, message):
        return self.log(self, message, severity=hou.severityType.Message)
    
    
    @staticmethod
    def _initFileSink():
        
        log_file = hou.text.expandString(Logger.log_file)
        
        file_sink = hou.logging.FileSink(log_file)
        file_sink.connect(Logger.source_name)
        
        return file_sink
    
    @staticmethod
    def _logToConsole(log_entry):
        message = log_entry.message()
        time    = log_entry.time()
        context = log_entry.sourceContext()
        severity = log_entry.severity()
        
        dt_object = datetime.datetime.fromtimestamp(time)
        time = dt_object.strftime("%H:%M:%S.%f")[:-3]

        severity = str(severity).split(".")[-1]

        print(time, severity, context, message)