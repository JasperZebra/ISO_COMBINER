def read_version_file():
    VERSION_PREFIX = "version="
    with open("config.txt", "r") as inf:
        line = inf.readline().strip()
        version = "" if not line.startswith(VERSION_PREFIX) else line[len(VERSION_PREFIX):]
    return version

def format_version_for_window(version):
    return f" v{version}"

def get_version():
    version = read_version_file()
    formatted_version = format_version_for_window(version)
    return formatted_version

def get_instructions():
    with open("application_instructions.txt", "r", encoding="utf-8") as inf:
        instructions = inf.read()
    return instructions
