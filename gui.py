import customtkinter as ctk
import os
import time
import threading
from tkinter import filedialog # Standard OS file picker
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend import FileOrganizer

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AgentHandler(FileSystemEventHandler):
    def __init__(self, app_instance):
        self.app = app_instance

    def on_created(self, event):
        if event.is_directory:
            return

        self.app.log_message(f"Detected: {os.path.basename(event.src_path)}")
        organizer = FileOrganizer()
        folder_path = os.path.dirname(event.src_path)
        
        time.sleep(0.5) 
        
        try:
            organizer.organize_folder(folder_path)
            self.app.log_message(f"Moved file to category folder.")
        except Exception as e:
            self.app.log_message(f"Error: {str(e)}")

class AgentGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Agent 007 - File Organizer")
        self.geometry("700x550")

        self.observer = None
        self.is_running = False
        
        # --- SMART PATH (Works on Windows & Linux) ---
        # Automatically finds the "Downloads" folder of whoever runs this
        self.default_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # --- UI Layout ---
        self.label_title = ctk.CTkLabel(self, text="FILE ORGANIZER AGENT", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=20)

        # Frame for Input + Browse Button
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10)

        self.entry_path = ctk.CTkEntry(self.input_frame, width=400, placeholder_text="Select Folder...")
        self.entry_path.insert(0, self.default_path) 
        self.entry_path.pack(side="left", padx=(0, 10))

        self.btn_browse = ctk.CTkButton(self.input_frame, text="Browse", width=100, command=self.browse_folder)
        self.btn_browse.pack(side="left")

        # Start/Stop Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.btn_start = ctk.CTkButton(self.button_frame, text="Start Agent", command=self.start_agent, fg_color="green")
        self.btn_start.pack(side="left", padx=10)

        self.btn_stop = ctk.CTkButton(self.button_frame, text="Stop Agent", command=self.stop_agent, fg_color="red", state="disabled")
        self.btn_stop.pack(side="left", padx=10)

        # Log Console
        self.label_log = ctk.CTkLabel(self, text="Mission Log:", font=("Roboto", 14))
        self.label_log.pack(pady=(20, 5), anchor="w", padx=50)

        self.log_box = ctk.CTkTextbox(self, width=600, height=250)
        self.log_box.pack(pady=10)
        self.log_box.insert("0.0", "System Ready. Waiting for command...\n")

    def browse_folder(self):
        # Opens the OS native folder picker
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, folder_selected)
            self.log_message(f"Target Changed: {folder_selected}")

    def log_message(self, message):
        self.after(0, self._update_log, message)

    def _update_log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{timestamp}] {message}\n")
        self.log_box.see("end")

    def start_agent(self):
        path = self.entry_path.get()
        if not os.path.exists(path):
            self.log_message("Error: Directory does not exist!")
            return

        self.is_running = True
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.entry_path.configure(state="disabled") # Lock the input while running
        self.btn_browse.configure(state="disabled") # Lock the browse button
        self.log_message(f"Agent 007 Started. Watching: {path}")

        self.thread = threading.Thread(target=self.run_watchdog, args=(path,), daemon=True)
        self.thread.start()

    def stop_agent(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        
        self.is_running = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.entry_path.configure(state="normal") # Unlock input
        self.btn_browse.configure(state="normal") # Unlock browse
        self.log_message("Agent 007 Stopped.")

    def run_watchdog(self, path):
        """The background worker process"""
        
        # --- PHASE 1: INITIAL CLEANUP (Batch Processing) ---
        # This handles files that are ALREADY in the folder
        self.log_message("Agent 007: Scanning existing files...")
        initial_organizer = FileOrganizer()
        
        try:
            # We run the organizer once immediately
            initial_organizer.organize_folder(path)
            self.log_message("Agent 007: Initial cleanup complete.")
        except Exception as e:
            self.log_message(f"Cleanup Error: {e}")

        # --- PHASE 2: REAL-TIME MONITORING (Interrupt Processing) ---
        # Now we start watching for NEW files
        event_handler = AgentHandler(self) 
        self.observer = Observer()
        self.observer.schedule(event_handler, path, recursive=False)
        self.observer.start()
        
        try:
            while self.is_running:
                time.sleep(1)
        except:
            self.observer.stop()

if __name__ == "__main__":
    app = AgentGUI()
    app.mainloop()