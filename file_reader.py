#######################################
# Literals & Constants
#######################################
VERSION=2.0
APP_INSTRUCTIONS = """
ISO Combiner Instructions:
1. Click 'Browse' and choose at least 2 .iso files to combine.
2. Click 'Combine' and name the new file. 
    *NOTE: Do not add the .iso extension to the file name.
3. You may need to refresh your file explorer if new file is not showing or if file size is empty.
"""

def read_version_file():
    return str(VERSION)

def format_version_for_window(version):
    return f" v{version}"

def get_version():
    version = read_version_file()
    formatted_version = format_version_for_window(version)
    return formatted_version

def get_instructions():
    return APP_INSTRUCTIONS
