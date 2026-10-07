import unittest
from datetime import datetime

from parsers.linux import LinuxParser
from event import Event, EventType

class TestLinuxParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = LinuxParser()
        
    def test_valid_logs(self):
        with open("logs/samples/linux/auth.log", "r") as file:
            lines = file.readlines()
            
        for line in lines:
            event = self.parser.parse(line.strip())
            
            self.assertIsInstance(event, Event)
            self.assertIsInstance(event.timestamp, datetime)
            self.assertEqual(event.source, "Linux")
            self.assertIsInstance(event.event_type, EventType)
            if event.username is not None:
                self.assertIsInstance(event.username, str)
            if event.source_ip is not None:
                self.assertIsInstance(event.source_ip, str)
            if event.process is not None:
                self.assertIsInstance(event.process, str)
            if event.pid is not None:
                self.assertIsInstance(event.pid, int)
            if event.message is not None:
                self.assertIsInstance(event.message, str)
            if event.event_id is not None:
                self.assertIsInstance(event.event_id, int)
            if event.log_name is not None:
                self.assertIsInstance(event.log_name, str)
                
    def test_invalid_logs(self):
        event = self.parser.parse("THIS IS NOT A VALID LOG FILE pid[12345] Linux")
        
        self.assertIsNone(event)
        
if __name__ == "__main__":
    unittest.main()