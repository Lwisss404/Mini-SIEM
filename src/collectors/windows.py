import subprocess
from typing import Iterator

from collectors.base import LogCollector


class WindowsCollector(LogCollector):
    
    def collect_recent(self, duration: str, log_names: list[str]) -> Iterator[str]:
        logs = " ,".join(
            f"'{log_name}'"
            for log_name in log_names
        )
        
        command = [
            "powershell",
            "-command",
            (
                f"logs = @({logs}); "
                f"Get-WinEvent -FilterHashtable @{{"
                f"LogName=$logs; "
                f"StartTime=(Get-Date).AddMinutes(-{duration})}} | ForEach-Object {{ "
                f"$_ | Select-Object TimeCreated, Id, ProviderName, ProcessId, LogName, Message | Convert-To Json -Compress }}"
            )            
        ]
        
        process = subprocess.Popen(
            command,
            stdout = subprocess.PIPE,
            suderr = subprocess.PIPE,
            text = True
        )
        
        try:
            for line in process.stdout:
                yield line.rstrip()
        finally:
            process.terminate()
            process.wait()
            
    def stream(self, log_names: list[str]) -> Iterator[str]:
        logs = " ,".join(
            f"'{log_name}'"
            for log_name in log_names
        )
        
        command = [
            "powershell",
            "-command",
            (
                f"$logs = @{logs}; "
                f"Register-WinEvent -LogName $logs -sSourceIdentifier 'MiniSIEM' | Our-Null; "
                f"try {{ "
                f"while ($true) {{ "
                f"$event = Wait-Event -SourceIdentifier 'MiniSIEM'; "
                f"$event.SourceEventArgs.EventRecord | Select-Object TimeCreated, Id, ProviderName, ProcessId, LogName, Message | ConvertTo-Json -Compress;"
                f"Remove-Event -EventIdentifier $event.EventIdentifier; "
                f"}}}} finally {{ "
                f"Unregister-Event -SourceIdentifier 'MiniSIEM' -ErrorAction SilentlyContinue"
            )
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
            
