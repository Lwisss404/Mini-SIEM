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
        process = match.group("process").strip()
        pid = int(match.group("pid")) if match.group("pid") else None
        message = match.group("message")
        
        event_type = LinuxParser.identify_event_type(process, message, 0)
        
        return Event(
            timestamp = timestamp.replace(year=datetime.now().year),
            source = "Linux",
            event_type = event_type,
            process = process,
            pid = pid,
            message = message
        )
        
    def identify_event_type(process: str, message: str, event_id: int) -> EventType:
        
        message = message.strip().lower()
        process = process.strip().lower()
        event_id = event_id
        
        if process in {"sshd", "login", "sudo", "su"}:
            if process != "su":
                if "accepted password" in message or "accepted publickey" in message or "accepted keyboard-interactive" in message or "authentication succeeded" in message or "session opened" in message:
                    return EventType.LOGIN_SUCCESS
            
            if process != "sudo":
                if "failed password" in message or "invalid user" in message or "authentication failure" in message or "authentication failed" in message or "failed su" in message:
                    return EventType.LOGIN_FAILURE
                
        if process in {"auditd", "audit", "systemd", "kernel"}:
            if "execve" in message or "syscall" in message or "process started" in message:
                return EventType.PROCESS_START
            
            if process != "audit":
                if "process exited" in message or "terminated" in message or "stopped" in message:
                    return EventType.PROCESS_STOP
            
        if process in {"sudo", "su", "pkexec", "doas"}:
            if "session opened" in message or "command=" in message or "authentication succeeded" in message or "executed" in message or "user=root" in message or "user root" in message:
                return EventType.PRIVILEGE_ESCALATION
            
        if process in {"useradd", "adduser", "usermod"}:
            if "new user" in message or "new group" in message or "added user" in message:
                return EventType.USER_CREATED
            
        if process in {"userdel", "deluser"}:
            if "deleted user" in message or "removed user" in message:
                return EventType.USER_DELETED
            
        if process in {"sshd", "login", "systemd-logind"}:
            if "logout" in message or "session closed" in message or "session disconnected" in message:
                return EventType.LOGOUT
        
        if process in {"auditd", "journald", "systemd"}:
            if "audit log cleared" in message:
                return EventType.LOG_CLEARED
        
        if process in {"sshd", "kernel", "NetworkManager"}:
            if "connection accepted" in message or "connection established" in message or "connection refused" in message or "connection from" in message:
                return EventType.NETWORK_CONNECTION