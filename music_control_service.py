import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes
import time

from app_service import open_application


# Music control functions
def control_music(action):
    """
    Controls music playback (play/pause, next, previous).
    """
    media_keys = {
        "play_pause": "playpause",
        "next": "nexttrack",
        "previous": "prevtrack"
    }
    if action in media_keys:
        pyautogui.press(media_keys[action])
        return f"Music {action.replace('_', ' ')} command executed."
    elif action == "play_in_spotify":
        open_application("spotify")
        time.sleep(3)
        pyautogui.press("playpause")
        return "Music play command executed."
    else:
        return "Invalid music control command."


# Volume control functions
def get_volume_interface():
    """
    Retrieves the volume interface from pycaw.
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))


def control_volume(action):
    """
    Controls system volume (increase, decrease, mute/unmute).
    """
    try:
        volume = get_volume_interface()

        if action == "mute":
            volume.SetMute(1, None)
            return "Volume muted."
        elif action == "unmute":
            volume.SetMute(0, None)
            return "Volume unmuted."
        elif action == "increase":
            current_volume = volume.GetMasterVolumeLevelScalar()
            volume.SetMasterVolumeLevelScalar(min(current_volume + 0.1, 1.0), None)
            return "Volume increased."
        elif action == "decrease":
            current_volume = volume.GetMasterVolumeLevelScalar()
            volume.SetMasterVolumeLevelScalar(max(current_volume - 0.1, 0.0), None)
            return "Volume decreased."
        elif action == "max":
            volume.SetMasterVolumeLevelScalar(1.0, None)
            return "Volume set to maximum."
        elif action == "half":
            volume.SetMasterVolumeLevelScalar(0.5, None)
            return "Volume set to 50%."
        elif action == "25%":
            volume.SetMasterVolumeLevelScalar(0.25, None)
            return "Volume set to 25%."
        elif action == "75%":
            volume.SetMasterVolumeLevelScalar(0.75, None)
            return "Volume set to 75%."
        else:
            return "Invalid volume control command."

    except Exception as e:
        return f"An error occurred: {e}"