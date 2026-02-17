 
# Agent 007: Intelligent File Organization System
**Operating System Mini-Project | Pop!OS Linux**

## 1. Project Overview
Agent 007 is a high-performance, event-driven file system utility designed to automate file organization. Unlike traditional scripts that require manual execution, this system operates as a background daemon, leveraging kernel-level interrupts to detect and organize files in real-time.

## 2. Technical Architecture
The system is built on a **Producer-Consumer Model**:
* **The Watchdog (Producer):** Uses the Linux `inotify` subsystem to monitor file system events (Creation/Modification).
* **The Engine (Consumer):** Analyzes file metadata (MIME types, extensions) and performs I/O operations (Move/Rename) to categorize files into `Images`, `Documents`, `Audio`, etc.
* **The GUI (Interface):** A multithreaded `CustomTkinter` interface that allows user interaction without blocking the background worker threads.

## 3. Key Features
* **Real-Time Monitoring:** Instant organization upon file drop.
* **Batch Processing:** Scans and cleans existing files on startup.
* **Concurrency:** Implements threading to keep the GUI responsive during heavy I/O operations.
* **Conflict Resolution:** Automatically handles duplicate filenames (e.g., `file(1).txt`).
* **Cross-Platform:** Smart path detection for Linux (Pop!OS) and Windows environments.

## 4. Technology Stack
* **Language:** Python 3.10+
* **GUI Framework:** CustomTkinter (Modern UI wrapper)
* **System Interface:** `watchdog` (Python API for `inotify`/`kqueue`)
* **Build Tool:** PyInstaller (for creating the standalone binary)

## 5. How to Run
### Method A: Standalone App (No Python Required)
1.  Navigate to the `dist` folder.
2.  Double-click the `Agent007` executable.
3.  Select a target folder and click **Start Agent**.

### Method B: Source Code

# Install dependencies
pip install customtkinter watchdog packaging

# Run the interface
python3 gui.py

6. Developer Notes
Resource Locking: The UI disables input fields while the agent is active to prevent race conditions.

Error Handling: The system logs all I/O errors to the GUI console without crashing the main process.

Developed by: F Lalthanmawia
