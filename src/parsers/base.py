from abc import ABC, abstractmethod
from typing import Optional

from event import Event

class LogParser(ABC):
    
    @abstractmethod
    def parse(self, line: str) -> Optional[Event]:
        """ Parse a raw log line into a normalized Event. """
        pass
    
