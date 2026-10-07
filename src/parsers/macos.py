import re
from datetime import datetime
from typing import Optional

from event import Event, EventType
from parsers.base import LogParser

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+ \S+)"
    r"\s+(?P<host>\S+)"
    r"\s+(?P<process>[^\[]+)"
    r"\[(?P<pid>\d+)\]:"
    r"\s+(?P<message>.*)$"
)

class MacOSParser(LogParser):

    def parse(self, line: str) -> Optional[Event]:
    
        match = LOG_PATTERN.match(line)

        if not match : return None
        
        timestamp = match.group("timestamp")
        if timestamp[-5] in "+-":
            timestamp = (timestamp[:-2] + ":" + timestamp[-2:])
            
        process = match.group("process").strip(),
        pid = int(match.group("pid")) if match.group("pid") else None
        message = match.group("message")

        event_type = MacOSParser.identify_event_type(process, message)

        return Event(
            timestamp = datetime.fromisoformat(timestamp),
            source = "MacOS",
            process = process,
            event_type = event_type,
            pid = pid,
            message = message
        )

    def identify_event_type(self, process: str, message: str) -> EventType:
        
        if "accepted password" in message:
            return EventType.LOGIN_SUCCESS
        
        if "failed password" in message:
            return EventType.LOGIN_FAILURE
    
        if process == "log" or process == "loginwindow":
            return EventType.LOGIN_SUCCESS
        return EventType.SYSTEM_EVENT
    

        