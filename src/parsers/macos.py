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
        timestamp = timestamp[:-5] + timestamp[-5:-2] + ":" + timestamp[-2:]

        return Event(
            timestamp = datetime.fromisoformat(timestamp),
            source = "MacOS",
            event_type = EventType.SYSTEM_EVENT,
            process = match.group("process").strip(),
            pid = match.group("pid"),
            message = match.group("message")
        )

    