import subprocess
from typing import Iterator

from collectors.base import LogCollector

class LinuxCollector(LogCollector):
    
    def collect_recent(self, duration: str) -> Iterator[str]:
        command = [
            "journalctl",
            "--since",
            duration,
            "--no-pager",
            "--output=short-iso"
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
            
        
    def stream(self) -> Iterator[str]:
        command = [
            "journalctl",
            "--follow",
            "--no-pager",
            "--output=short-iso"
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
        