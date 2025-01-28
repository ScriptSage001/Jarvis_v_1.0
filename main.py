from sys import exit
import threading
import time
import speech_recognition as sr
import webbrowser as wb

import music_library as ml
from tts_engine_service import speak
from app_service import open_application, refresh_installed_apps, close_application
from music_control_service import control_music, control_volume
from youtube_service import play_on_youtube
from spotify_service import search_and_play_on_spotify, spotify_controls
from search_service import search


def music_control(command):
    """
    Control volume.
    """
    try:
        # Music controls
        if ("play music" in command and "spotify" not in command) or "pause music" in command:
            print(control_music("play_pause"))
            return True
        elif "next song" in command:
            print(control_music("next"))
            return True
        elif "previous song" in command:
            print(control_music("previous"))
            return True
        elif "play music in spotify" in command:
            print(control_music("play_in_spotify"))
            return True
        elif "play" == command.strip():
            spotify_controls("play")
            return True
        elif "pause" == command.strip():
            spotify_controls("pause")
            return True
        elif "next" == command.strip():
            spotify_controls("next")
            return True
        elif "previous" == command.strip():
            spotify_controls("previous")
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def volume_control(command):
    """
    Control volume.
    """
    try:
        # Volume controls
        if "mute volume" in command:
            print(control_volume("mute"))
            return True
        elif "unmute volume" in command:
            print(control_volume("unmute"))
            return True
        elif "increase volume" in command:
            print(control_volume("increase"))
            return True
        elif "decrease volume" in command:
            print(control_volume("decrease"))
            return True
        elif "volume max" in command:
            print(control_volume("max"))
            return True
        elif "volume 50%" in command:
            print(control_volume("half"))
            return True
        elif "volume 25%" in command:
            print(control_volume("25%"))
            return True
        elif "volume 75%" in command:
            print(control_volume("75%"))
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def process_command(command):
    """Process and execute commands."""
    command = command.lower()
    if command.startswith("open"):
        target = command[5:].strip().lower()
        is_admin_mode = 'as administrator' in target

        if is_admin_mode:
            target = target.replace("as administrator", "").strip()
            open_application(target, is_admin_mode = True)
        else:
            open_application(target)

    elif command.startswith("close"):
        target = command[6:].strip().lower()
        close_application(target)

    elif (command.startswith("play")
          and "music" not in command
          and command.strip() != "play"):
        song = command[5:].strip()
        if song in ml.music.keys():
            speak(f"Playing {song}")
            wb.open(ml.music[song])
        elif "on youtube" in command:
            play_on_youtube(command)
        elif "on spotify" in command:
            search_and_play_on_spotify(command)
        else:
            speak(f"Sorry, I do not have {song} in my library")

    elif music_control(command):
        pass

    elif volume_control(command):
        pass

    elif "search" in command:
        search(command)

    elif "exit" in command or "quit" in command:
        speak("Goodbye, sir!")
        exit()
    else:
        speak("Sorry, I didn't understand that.")

def recognize_speech(recognizer, microphone, language = "en-US", wake_call = False):
    """Recognize speech from the microphone."""
    try:
        print("Listening...")
        if wake_call:
            audio = recognizer.listen(microphone, timeout = 5, phrase_time_limit = 5)

        else:
            # Increase to handle long pauses
            recognizer.pause_threshold = 2

            # Adjust for noisy environments
            recognizer.energy_threshold = 300

            audio = recognizer.listen(microphone, timeout = 5, phrase_time_limit = 10)

        return recognizer.recognize_google(audio, language = language)
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
        return None
    except sr.WaitTimeoutError:
        print("No speech detected.")
        return None

def background_refresh(interval = 3600):
    """
    Background thread to refresh the installed apps list periodically.
    """
    while True:
        time.sleep(interval)
        refresh_installed_apps()
        print("Installed apps list refreshed in the background.")


if __name__ == "__main__":
    # Initialize Jarvis
    speak("Initializing Jarvis")
    refresh_installed_apps()
    recognizer = sr.Recognizer()

    # Start background thread for periodic app list refresh
    threading.Thread(target = background_refresh, daemon = True).start()

    with sr.Microphone() as mic:
        # Calibrate the recognizer for ambient noise
        recognizer.adjust_for_ambient_noise(mic, duration = 1)
        # recognizer.dynamic_energy_threshold = True

        speak("Jarvis is ready. Say 'Jarvis' to wake up.")

        while True:
            # Listen for the wake word
            wake_word = recognize_speech(recognizer, mic, "en-in", True)
            if wake_word and "jarvis" in wake_word.lower():
                # speak("Yes sir, how can I help you?")
                speak("Yes sir")
                # Ask for a command
                command = recognize_speech(recognizer, mic, "en-in")

                if command:
                    process_command(command)
                else:
                    speak("I didn't hear a valid command. Please try again.")

            # Add a brief pause to avoid constant "no speech detected"
            print("Waiting for the next command...")