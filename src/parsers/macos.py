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
            
        process = match.group("process").strip()
        pid = int(match.group("pid")) if match.group("pid") else None
        message = match.group("message")

        event_type = MacOSParser.identify_event_type(process, message, 0)

        return Event(
            timestamp = datetime.fromisoformat(timestamp),
            source = "MacOS",
            process = process,
            event_type = event_type,
            pid = pid,
            message = message
        )

    def identify_event_type(process: str, message: str, event_id: int) -> EventType:
        
        message = message.lower()
        process = process.strip().lower()
        event_id = event_id
        
        if process in {"sshd", "loginwindow", "securityd"}:
            if "accepted password" in message or "accepted publickey" in message or "authentication succeeded" in message:
                return EventType.LOGIN_SUCCESS

            if "failed password" in message or "authentication failure" in message or "authentication failed" in message:
                return EventType.LOGIN_FAILURE
            
        if process in {"launchd", "runningboardd", "launchservicesd"}:
            if "started" in message or "launching" in message or "spawned" in message or re.search(r"process .* started", message) or "job state = running" in message or "service state: running" in message:
                return EventType.PROCESS_START
            
            if process != "launchservicesd":
                if "service state: not running" in message or "sevice only ran for 0 seconds":
                    return EventType.PROCESS_STOP
                
        if process in {"sudo", "su"}:
            if "authentication succeeded" in message or "command" in message or "TTY" in message or re.search(r"user .* executed", message):
                return EventType.PRIVILEGE_ESCALATION
            
        if process in {"opendirectoryd", "dscl"}:
            if "account created" in message or "created account" in message or "created user" in message or "create user" in message or "new user" in message:
                return EventType.USER_CREATED
            
            if process != "dscl":
                if "deleted user" in message or "removed user" in message or "delete user" in message:
                    return EventType.USER_DELETED
        
        if process in {"loginwindow", "sshd"}:
            if "logged out" in message or "session closed" in message or "session terminated" in message:
                return EventType.LOGOUT
            
        """ here rule for LOG_CLEARED event type """
        """ No reliable way to detect user/admin log clearance """

        if process in {"networkd", "nesessionmanager", "socketfilterfw"}:
            if "connection accepted" in message or "connection refused" in message or "connection established" in message:
                return EventType.NETWORK_CONNECTION
        
        return EventType.SYSTEM_EVENT