from labeeb.services.platform_services.common import platform_utils

def clear_terminal():
    import os

    os.system("cls" if os.name == "nt" else "clear")
