import os
import subprocess
import win32com.client
import webbrowser as wb

# Dictionary of known apps with their paths
KNOWN_APPS = {
    "notepad": r"C:\\Windows\\System32\\notepad.exe",
    "terminal": r"C:\\Windows\\System32\\cmd.exe",
    "calculator": r"C:\\Windows\\System32\\calc.exe",
    "microsoft edge": r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
}

# Dictionary of common websites with URLs
COMMON_WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "linkedin": "https://www.linkedin.com",
    "twitter": "https://www.twitter.com"
}

# Installed apps
INSTALLED_APPS = {}

def get_installed_apps():
    """Get installed apps by scanning Start Menu shortcuts."""
    installed_apps = {}
    shell = win32com.client.Dispatch("WScript.Shell")

    # Paths to Start Menu folders
    start_menu_paths = [
        os.path.expandvars("%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"),
        os.path.expandvars("%PROGRAMDATA%\\Microsoft\\Windows\\Start Menu\\Programs")
    ]

    for path in start_menu_paths:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".lnk"):
                    shortcut = os.path.join(root, file)
                    try:
                        shortcut_obj = shell.CreateShortcut(shortcut)
                        installed_apps[file[:-4].lower()] = shortcut_obj.TargetPath
                    except Exception as e:
                        print(f"Error processing shortcut {shortcut}: {e}")
    return installed_apps

def refresh_installed_apps():
    """
    Refresh the global installed apps list by rescanning the Start Menu.
    """
    global INSTALLED_APPS
    INSTALLED_APPS = get_installed_apps()

def open_application(app_name):
    """Open an application based on the app name."""
    try:
        # Check in known apps
        if app_name in KNOWN_APPS:
            subprocess.Popen(KNOWN_APPS[app_name])
            return

        # Check in installed apps
        if app_name in INSTALLED_APPS:
            subprocess.Popen(INSTALLED_APPS[app_name])
            return

        # Check in common websites
        if app_name in COMMON_WEBSITES:
            wb.open(COMMON_WEBSITES[app_name])
            return

        # If not found
        print(f"Sorry, I couldn't find {app_name}.")
    except Exception as e:
        print(f"Failed to open {app_name}. Error: {e}")
