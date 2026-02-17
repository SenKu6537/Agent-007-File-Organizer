import sys
import time
import os  # Moved to top so 'Handler' can use it
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend import FileOrganizer 

# --- The Event Handler (The Logic) ---
class Handler(FileSystemEventHandler):
    def on_created(self, event):
        # This function runs ONLY when the OS detects a file creation
        if event.is_directory:
            return None

        print(f"Target Acquired: {event.src_path}")
        
        # 1. Instantiate the organizer engine
        organizer = FileOrganizer()
        
        # 2. Get the folder path
        # We need to ensure we are passing the directory, not the file itself
        folder_path = os.path.dirname(event.src_path)
        
        # 3. Trigger the organization
        print("Agent 007: Engaging File Organizer...")
        organizer.organize_folder(folder_path)

# --- The Watcher Service (The Background Process) ---
class Agent007:
    # Set the directory to watch
    watchDirectory = "/home/ballsack/Developer/test_chaos" 
    
    def __init__(self):
        self.observer = Observer()
        
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        print(f"OS Watchdog Agent 007: Monitoring {self.watchDirectory}...")
        try:
            while True:
                time.sleep(5) # Keeping Agent 007 active
        except KeyboardInterrupt:
            self.observer.stop()
            print("Agent 007 Stopped")
            
        self.observer.join()

if __name__ == '__main__':
    # Instantiate the class 
    watch = Agent007()
    
    # Run the agent
    watch.run()