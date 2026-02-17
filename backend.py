import os
import shutil
from pathlib import Path

class FileOrganizer:
    def __init__(self):
        #Define your file type categories (The Rules)
        self.DIRECTORIES = {
            "Images" : [".jpg",".jpeg", ".png", ".gif", ".bmp", ".svg"],
            "Documents" : [".bat",".pdf", ".docx", ".txt", ".pptx", ".xlsx", ".csv"],
            "Archives" : [".zip", ".tar",".gz",".rar"],
            "Audio" : [".m4a",".mp3",".wav",".aac"],
            "Video" : [".mp4",".mov",".mkv",".avi"],
            "Scripts" : [".py",".js",".c",".html",".css",".cpp",".bash",".sh"]
        
        }
        
        # Fallback folder for unknown file types
        self.OTHER_DIR = "Others"
        
    def get_unique_filename(self, destination, filename):
        #Handles name cillisions. If 'file.txt' exists, returns 'file(1).txt
        base, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        
        #Check if file exists in destination path
        while os.path.exists(os.path.join(destination, new_filename)):
            new_filename = f"{base}({counter}){extension}"
            counter += 1
            
        return new_filename

    def organize_folder(self, source_path):
        #The main engine. Scans the filder and moves files. Returns a lig of actions taken
        actions_log = []
        
        if not os.path.exists(source_path):
            return["Error: Source path does not exist."]
        
        # 1. Directory traverrsai, the scanner
        # We use scandir for better perormance on large directories 
        with os.scandir(source_path) as entries:
            for entry in entries:
                if entry.is_file():
                    self._process_file(entry, source_path, actions_log)
        return actions_log
    
    def _process_file(self,entry,source_path,log):
        filename = entry.name
        file_path = entry.path
        
        #w. Metadata analysis (get extension)
        # lowe() ensures .JPG and .jpg are treated the same
        _, extension = os.path.splitext(filename)
        extension = extension.lower()
        
        #3. Decision Logic (Where does it go?)
        destination_folder_name = self.OTHER_DIR
        found = False
        
        for folder, ext_list in self.DIRECTORIES.items():
            if extension in ext_list:
                destination_folder_name = folder
                found = True
                break
            
        #4. I/O operation (The move)
        destination_path = os.path.join(source_path,destination_folder_name)
        
        # Create the sub_directory if it doesn't exist
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
            
        # Handle duplicate fielnames
        unique_name = self.get_unique_filename(destination_path, filename)
        final_dest_path = os.path.join(destination_path, unique_name)
        
        try:
            shutil.move(file_path, final_dest_path)
            log.append(f"moved: {filename} -> {destination_folder_name}/{unique_name}:")
        
        except Exception as e:
            log.append(f"Error moving {filename} : {str(e)}")
            
# -- Test Area (Runs only if you execute this file directly)---

if __name__ == "__main__":
    #Create a dummy organizer and run it purely for testing
    organizer = FileOrganizer()
    
    #Input test folder path here
    #Windows example: r"C:\Users\YourName\Desktop\TestFolder"
    #linux example: "/Users/YourName/Desktop/TestFolder"
    
    target_dir = input("Enter full path of folder to organize: ").strip().replace(' " ', ' ')
    
    print(f"Scanning {target_dir}...")
    logs = organizer.organize_folder(target_dir)
    
    for line in logs:
        print(line)
        
    print("Done")

            
        