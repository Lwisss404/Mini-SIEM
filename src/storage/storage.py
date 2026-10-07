import sqlite3
import sys
import hashlib

from event import Event

class Storage():
    
    def initialize_database():
        print("Initializing Database...")
        try:
            with sqlite3.connect("../logs/siem.db") as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """ CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fingerprint varchar(64) UNIQUE,
                        timestamp DATETIME,
                        source varchar(32),
                        event_type varchar(32),
                        username varchar(255),
                        source_ip varchar(32),
                        process varchar(255),
                        pid INT,
                        message TEXT,
                        event_id INT,
                        log_name varchar(255))
                """)
                connection.commit()
        except sqlite3.Error as error:
            print(f"Error Creating Database: {error}", file=sys.stderr)
            raise error
            
    def save_event(event: Event):
        try:
            with sqlite3.connect("../logs/siem.db") as connection:
                fingerprint = Storage.hash(event)
                cursor = connection.cursor()
                try:        
                    cursor.execute(
                        """ INSERT INTO logs (fingerprint, timestamp, source, event_type, username, source_ip, process, pid, message, event_id, log_name) 
                            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """ , 
                        (fingerprint, event.timestamp.isoformat(), event.source, event.event_type.value, event.username, 
                         event.source_ip, event.process, event.pid, event.message, event.event_id, event.log_name)
                    )
                    connection.commit()
                except sqlite3.IntegrityError:
                    print("Duplicated Log entry Ignored!")
        except sqlite3.Error as error:
            print(f"Error Inserting Log Entry: {error}", file=sys.stderr)
            raise error
    
    def hash(event : Event) -> str:
        fingerprint = hashlib.sha256()
        fingerprint.update(event.timestamp.isoformat().encode())
        fingerprint.update(event.source.encode('utf-8'))
        if event.event_id != None: fingerprint.update(event.event_id.to_bytes(length=8, byteorder='big'))
        if event.log_name != None: fingerprint.update(event.log_name.encode('utf-8'))
        """print(f"#DEBUG: {event.pid}")"""
        """print(f"#DEBUG: {type(event.pid)}")"""
        if event.pid != None: fingerprint.update(event.pid.to_bytes(length=8, byteorder='big'))
        if event.message != None: fingerprint.update(event.message.encode('utf-8'))
        return fingerprint.hexdigest()