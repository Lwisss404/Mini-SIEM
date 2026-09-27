import subprocess
from typing import Iterator

from collectors.base import LogCollector

class MacOSCollector(LogCollector):
    
    def collect_recent(self, duration: str) -> Iterator[str]:
        command = [
            "log",
            "show",
            "--last",
            duration,
            "--style",
            "syslog"
        ]
        
        process = subprocess.Popen(
            command,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True
        )
        
        for line in process.stdout:
            yield line.rstrip()
        
    def stream(self) -> Iterator[str]:
        command = [
            "log",
            "stream",
            "--style",
            "syslog"
        ]
        
        process = subprocess.Popen(
            command,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True
        )
        
        try:
            for line in process.stdout:
                yield line.rstrip()   
        finally:
            process.terminate()
            process.wait()