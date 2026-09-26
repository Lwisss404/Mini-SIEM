from datetime import datetime
from event import Event, EventType



def main():
    
    event = Event (
        timestamp = datetime.now(),
        source = "MacOS",
        event_type = EventType.LOGIN_SUCCESS,
        username = "root",
        source_ip = "192.82.56.101",
        process = "sshd",
        message = "Failed Password For Root"
    )    
    
    print(event)



if __name__ == "__main__":
    main()