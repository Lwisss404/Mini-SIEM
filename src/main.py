import platform

from collectors.macos import MacOSCollector
from collectors.linux import LinuxCollector
from collectors.windows import WindowsCollector
from parsers.macos import MacOSParser
from parsers.linux import LinuxParser
from parsers.windows import WindowsParser
from interface.interface import Interfaces
from storage.storage import Storage


def main():
    
    system = platform.system()
    
    Storage.initialize_database()
    
    if system == "Darwin":
        print("Running On MacOS...")
        collector = MacOSCollector()
        parser = MacOSParser()
        if Interfaces.interface_capture_mode() == 2:
            try:
                for line in collector.stream():
                    event = parser.parse(line)
                    if event:
                        print("\n")
                        print(event)
                        Storage.save_event(event)
            except KeyboardInterrupt:
                print("\nStopping log stream...")
        else:
            time = f"{Interfaces.interface_log_age_input()}m"
            for line in collector.collect_recent(time):
                event = parser.parse(line)
                if event:
                    print("\n")
                    print(event)
                    Storage.save_event(event)
    
    elif system == "Linux":
        print("Running On Linux...")
        collector = LinuxCollector()
        parser = LinuxParser()
        if Interfaces.interface_capture_mode() == 2:    
            try:
                for line in collector.stream():
                    event = parser.parse(line)
                    if event:
                        print("\n")
                        print(event)
                        Storage.save_event(event)
            except KeyboardInterrupt:
                print("\nStopping log stream...")
        else:
            time = f"{Interfaces.interface_log_age_input()}m"
            for line in collector.collect_recent(time):
                event = parser.parse(line)
                if event:
                    print("\n")
                    print(event)
                    Storage.save_event(event)
            
    elif system == "Windows":
        print("Running On Windows...")
        collector = WindowsCollector()
        parser = WindowsParser()
        if Interfaces.interface_capture_mode() == 2:
            try:
                for line in collector.stream():
                    event = parser.parse(line)
                    if event:
                        print("\n")
                        print(event)
                        Storage.save_event(event)
            except KeyboardInterrupt:
                print("\nStopping log stream...")
        else:
            time = f"{Interfaces.interface_log_age_input()}m"
            for line in collector.collect_recent(time):
                event = parser.parse(line)
                if event:
                    print("\n")
                    print(event)
                    Storage.save_event(event)
    
    else: print(f"Unsupported Operating System: {system}")
    



if __name__ == "__main__":
    main()