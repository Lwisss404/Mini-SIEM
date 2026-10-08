from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class EventType(Enum):
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILURE = "LOGIN_FAILURE"
    PROCESS_START = "PROCESS_START"
    PROCESS_STOP = "PROCESS_STOP"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"
    USER_CREATED = "USER_CREATED"
    USER_DELETED = "USER_DELETED"
    LOGOUT = "LOGOUT"
    LOG_CLEARED = "LOG_CLEARED"
    NETWORK_CONNECTION = "NETWORK_CONNECTION"
    SYSTEM_EVENT = "SYSTEM_EVENT"


@dataclass
class Event:
    timestamp: datetime
    source: str
    event_type: EventType
    username: Optional[str] = None
    source_ip: Optional[str] = None
    process: Optional[str] = None
    pid: Optional[int] = None
    message: Optional[str] = None
    event_id: Optional[int] = None
    log_name: Optional[str] = None
    
