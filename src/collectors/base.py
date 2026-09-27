from abc import ABC, abstractmethod
from typing import Iterator

class LogCollector(ABC):
    
    @abstractmethod
    def collect_recent(self, duration: str) -> Iterator[str]:
        """ Collect existing logs for the given time period. """
        pass
    
    @abstractmethod
    def stream(self) -> Iterator[str]:
        """ Stream new log entries as they are generated. """
        pass