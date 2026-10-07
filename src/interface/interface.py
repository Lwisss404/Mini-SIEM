class Interfaces():
    
    def interface_capture_mode() -> int:
        choice: int
        print("===== Capture Mode Selection Menu =====")
        while True:
            print("1. Recent Logs")
            print("2. Stream Logs")
            choice = int(input("Select Capture Mode: "))
            if str(choice) in "12": return choice 
            else: print("Invalid Selection, Try Again!")
            
    def interface_log_age_input() -> int:
        choice: int
        while True:
            choice = int(input("Since how long should the logs be captured (in minutes): "))
            if choice > 0: return choice
            else: print("Time Cannot Be Negative Or Zero, Try Again!")
            
    def interface_windows_log_channel() -> list[str]:
        choice: int
        print("=== Windows Log Channel Selection Menu ===")
        list = []
        while True:
            print("1. Application")
            print("2. Security")
            print("3. System")
            choice = int(input("Select Log Channel: "))
            if choice == 1: list.append("Application")
            elif choice == 2: list.append("Security")
            elif choice == 3: list.append("System")
            else: print("Invalid Selection, Try Again!")