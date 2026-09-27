from datetime import datetime

from event import Event, EventType
from parsers.macos import MacOSParser
from collectors.macos import MacOSCollector


def main():
    
    collector = MacOSCollector()
    parser = MacOSParser()
    
    """for line in collector.collect_recent("5m"):
        print(line)"""
        
    try:
        for line in collector.stream():
            event = parser.parse(line)
            if event:
                print("\n")
                print(event)
    
    except KeyboardInterrupt:
        print("\nStopping log stream...")



if __name__ == "__main__":
    main()