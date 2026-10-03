import unittest
from datetime import datetime

from parsers.macos import MacOSParser
from event import Event, EventType

class TestMacOSParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = MacOSParser()
        
    def test_valid_logs(self):
        with open("samples/macos/system.log", "r") as file:
            lines = file.readlines()
            
        for line in lines:
            event = self.parser.parse(line.strip())
            
            self.assertIsInstance(event, Event)
            self.assertIsInstance(event.timestamp, datetime)
            self.assertEqual(event.source, "MacOS")
            self.assertIsInstance(event.event_type, EventType)
            if event.username is not None:
                self.assertIsInstance(event.username, str)
            if event.source_ip is not None:
                self.assertIsInstance(event.source_ip, str)
            if event.process is not None:
                self.assertIsInstance(event.process, str)
            if event.pid is not None:
                self.assertIsInstance(event.pid, str)
            if event.message is not None:
                self.assertIsInstance(event.message, str)
            if event.event_id is not None:
                self.assertIsInstance(event.event_id, int)
            if event.log_name is not None:
                self.assertIsInstance(event.log_name, str)
    
    def test_invalid_logs(self):
        event = self.parser.parse("THIS IS REALLY NOT A VERY VALID LOG ENTRY AM I RIGHT localhost pid[3425] very serious message")
        
        self.assertIsNone(event)
        
if __name__ == "__main__":
    unittest.main()