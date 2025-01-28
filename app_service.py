import os
import subprocess
import win32com.client
import webbrowser as wb
import psutil

# Dictionary of known apps with their paths
KNOWN_APPS = {
    "notepad": r"C:\\Windows\\System32\\notepad.exe",
    "notepad plus plus": r"C:\Program Files\Notepad++\notepad++.exe",
    "terminal": r"wt",
    "calculator": r"C:\\Windows\\System32\\calc.exe",
    "edge": r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "whatsapp": r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2503.5.0_x64__cv1g1gvanyjgm\WhatsApp.exe",
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
INSTALLED_APPS = None

def get_installed_apps():
    global INSTALLED_APPS
    if INSTALLED_APPS is not None:
        return INSTALLED_APPS

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
    INSTALLED_APPS = installed_apps
    return installed_apps

def refresh_installed_apps():
    """
    Refresh the global installed apps list by rescanning the Start Menu.
    """
    global INSTALLED_APPS
    INSTALLED_APPS = None
    get_installed_apps()

def open_application(app_name, is_admin_mode = False):
    """Open an application based on the app name."""
    try:

        app_path = None

        # Check in known apps
        app_path = KNOWN_APPS.get(app_name) or INSTALLED_APPS.get(app_name)

        if app_path:
            try:
                if is_admin_mode:
                    subprocess.run(
                        ["powershell", "Start-Process", f'"{app_path}"', "-Verb", "runAs"],
                        shell=True,
                    )
                else:
                    subprocess.Popen(app_path, shell=True)
                return
            except Exception as e:
                print(f"Error opening application '{app_name}': {e}")
        else:
            launch_website(app_name)

        # If not found
        print(f"Sorry, I couldn't find {app_name}.")
    except Exception as e:
        print(f"Failed to open {app_name}. Error: {e}")

def launch_website(website):
    """Launch a website in the default browser."""
    url = COMMON_WEBSITES.get(website)
    if url:
        wb.open(url)
    else:
        print(f"Sorry, I'm unable to open {website}.")

def close_application(app_name):
    """Closes an application by its name."""
    for process in psutil.process_iter(attrs = ["pid", "name"]):
        if process.info["name"] and app_name in process.info["name"].lower():
            try:
                process.terminate()  # Gracefully terminate the process
                print(f"{app_name} has been terminated.")
                return
            except psutil.AccessDenied:
                print(f"Access denied while trying to terminate {app_name}. Try running as administrator.")
                return
            except Exception as e:
                print(f"Error: {e}")
                return
    print(f"No running process found with the name {app_name}.")