#######################################
# Literals & Constants
#######################################
VERSION=3.0
APP_INSTRUCTIONS = """
ABOUT THIS APPLICATION:
ISO COMBINER combines game files in format of .iso on Windows machines.
This application can combine .iso files for multiple games at the same time.

PREREQUISITES AND IMPORTANT INFO:
1. This only works on Windows machines
2. The program creates copies of .iso files in order to combine them and save them on your machine. Please ensure you have enough memory available on your machine to succesfully combine the .iso files.
3. All .iso files from the same game must have the same GAMEID in the file name.
    
    Example: 
    GAME1.part0.iso and GAME1.part1.iso are files for the same game.
    GAME2.part0.iso and GAME2.part1.iso are files for another game.
    If all four files are selected, the end result will be two files:
    GAME1.COMBINED.iso and GAME2.COMBINED.iso

4. If the new combined .iso file has "0 bytes" or is not displaying in your file explorer properly, please refresh or close and reopen your file explorer. 
5. If the new combined .iso is on your Desktop, right click your Desktop and select the "refresh" button.
6. A message will display at the end of the process detailing any errors or failures for each game. If all games succeed, a SUCCESS message will display at the top. If any fail, a FAILED message will display. More details on which specific games failed will appear in the message box.
7. If any .iso files fail to combine, the process will stop for all games as this usually indicates that your machine is out of memory. An exact error message will be displayed at the end.

INSTRUCTIONS:
1. Click the "Browse" button to select the .iso files that you want to combinee.
    Use the "Clear" button as needed to remove unwanted files from the window.
2. Click the "Combine" button to combine the selected files.
    Only files from the same games will be combined together. 
    (see #3 under Prerequisites and important information for details)
3. The resulting combined .iso files will automatically be loaded into the path of the first file selected for each game.
4. After loading, a message box will display a success/failure message confirming if the .iso files have been combined successfully.

For more details and help, visit: https://github.com/JasperZebra/ISO_COMBINER
"""

#######################################
# File reading utils
#######################################
import os
from collections import defaultdict

def read_version_file():
    return str(VERSION)

def format_version_for_window(version):
    return f" v{version}"

def get_version():
    version = read_version_file()
    formatted_version = format_version_for_window(version)
    return formatted_version

def get_instructions_text():
    return APP_INSTRUCTIONS

def extract_filename(file_path):
    file_name_with_extension = os.path.basename(file_path)
    file_name, _ = os.path.splitext(file_name_with_extension)
    return file_name.rsplit(".part", 1)[0]

def get_game_name_to_file_paths_map(file_paths):
    game_name_to_file_path = defaultdict(list)
    for file_path in file_paths:
        game_name = extract_filename(file_path)
        game_name_to_file_path[game_name].append(file_path)
    return game_name_to_file_path

def create_unique_filename(file_path):
    base_name, extension = os.path.splitext(file_path)
    unique_name = file_path
    counter = 1
    while os.path.exists(unique_name):
        unique_name = f"{base_name}.COMBINED.({counter}){extension}"
        counter += 1
    return unique_name

