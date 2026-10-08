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
        event_id = data["Id"]
        log_name = data["ProviderName"]
        pid = data["ProcessId"]
        message = data["Message"]
        
        event_type = WindowsParser.identify_event_type("", message, event_id)
        
        return Event(
            timestamp = datetime.fromisoformat(timestamp_string),
            source = "Windows",
            event_type = event_type,
            event_id = event_id,
            log_name = log_name,
            pid = pid,
            message = message
        )
        
    def identify_event_type(process: str, message: str, event_id: int) -> EventType:
        
        message = message.strip().lower()
        process = process.strip().lower()
        
        if event_id == 4624: return EventType.LOGIN_SUCCESS
        if event_id == 4625: return EventType.LOGIN_FAILURE
        if event_id == 4634 or event_id == 4647: return EventType.LOGOUT
        if event_id == 4688: return EventType.PROCESS_START
        if event_id == 4689: return EventType.PROCESS_STOP
        if event_id == 4672: return EventType.PRIVILEGE_ESCALATION
        if event_id == 4720: return EventType.USER_CREATED
        if event_id == 4726: return EventType.USER_DELETED
        if event_id == 1102: return EventType.LOG_CLEARED
        