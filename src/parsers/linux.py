import re
from datetime import datetime
from typing import Optional

from event import Event, EventType
from parsers.base import LogParser

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\w{3}\s+\d{1,2}\s+\S+)"
    r"\s+(?P<host>\S+)"
    r"\s+(?P<process>[^\[]+)"
    r"\[(?P<pid>\d+)\]:"
    r"\s+(?P<message>.*)$"
)

class LinuxParser(LogParser):
    
    def parse(self, line: str) -> Optional[Event]:
        
        match = LOG_PATTERN.match(line)
        
        if not match: return None
        
        timestamp = datetime.strptime(match.group("timestamp"), "%b %d %H:%M:%S")
        pid = match.group("pid")
        
        return Event(
            timestamp = timestamp.replace(year=datetime.now().year),
            source = "Linux",
            event_type = EventType.SYSTEM_EVENT,
            process = match.group("process").strip(),
            pid = int(pid) if pid else None,
            message = match.group("message")
        )