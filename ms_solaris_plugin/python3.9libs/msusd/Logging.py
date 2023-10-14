"""
CODE FROM SIDEFX FORUM, NOT IMPLEMENTED
https://www.sidefx.com/forum/topic/81586/?page=1#post-367977
"""

import hou
import logging

HOU_SEVERITY_MAP = {
    logging.DEBUG: hou.severityType.Message,
    logging.INFO: hou.severityType.ImportantMessage,
    logging.WARNING: hou.severityType.Warning,
    logging.ERROR: hou.severityType.Error,
    logging.CRITICAL: hou.severityType.Fatal,
}


class HouLogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(self)

    def emit(self, record: logging.LogRecord):
        hlog_entry = hou.logging.LogEntry(
            record.msg,
            source_context=record.name,
            severity=HOU_SEVERITY_MAP[record.levelno],
            thread_id=record.thread,
        )
        hou.logging.log(hlog_entry)


logger = logging.getLogger("MsUsd")
logger.handlers = [HouLogHandler()]  # addHandler in actual code
logger.setLevel(logging.DEBUG)
