from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class EventType(Enum):
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILURE = "LOGIN_FAILURE"
    PROCESS_START = "PROCESS_START"
    PROCESS_STOP = "PROCESS_STOP"


@dataclass
class Event:
    timestamp: datetime
    source: str
    event_type: EventType
    username: Optional[str] = None
    source_ip: Optional[str] = None
    process: Optional[str] = None
    message: Optional[str] = None
    
