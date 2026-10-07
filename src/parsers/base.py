from abc import ABC, abstractmethod
from typing import Optional

from event import Event, EventType

class LogParser(ABC):
    
    @abstractmethod
    def parse(self, line: str) -> Optional[Event]:
        """ Parse a raw log line into a normalized Event. """
        pass
    
    @abstractmethod
    def identify_event_type(self, process: str, message: str) -> EventType:
        """ Identify the event type according to the content of precific fields of event """
        pass
    
