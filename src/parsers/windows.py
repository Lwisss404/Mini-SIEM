import json
from datetime import datetime
from typing import Optional

from parsers.base import LogParser
from event import Event, EventType


class WindowsParser(LogParser):
    
    def parse(self, line: str) -> Optional[Event]:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            return None
        
        timestamp_string = data["TimeCreated"]
        if "." in timestamp_string:
            prefix, rest = timestamp_string.split(".", 1)
            fractional = rest[:6]
            timezone = rest[7:]
        timestamp_string = f"{prefix}.{fractional}{timezone}"
        
        return Event(
            timestamp = datetime.fromisoformat(timestamp_string),
            source = "Windows",
            event_type = EventType.SYSTEM_EVENT,
            event_id = data["Id"],
            log_name = data["ProviderName"],
            pid = data["ProcessId"],
            message = data["Message"]
        )
        
