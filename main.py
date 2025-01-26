import threading
import time

import speech_recognition as sr
import webbrowser as wb
import pyttsx3 as tts
import music_library as ml
import app_service

# Initialize text-to-speech engine
engine = tts.init()


def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()


def process_command(command):
    """Process and execute commands."""
    command = command.lower()
    if command.startswith("open"):
        target = command[5:].strip().lower()
        app_service.open_application(target)

    elif command.startswith("play"):
        song = command[5:].strip()
        if song in ml.music.keys():
            speak(f"Playing {song}")
            wb.open(ml.music[song])
        else:
            speak(f"Sorry, I do not have {song} in my library")
    elif "exit" in command or "quit" in command:
        speak("Goodbye, sir!")
        exit()
    else:
        speak("Sorry, I didn't understand that.")


def recognize_speech(recognizer, microphone, language="en-US"):
    """Recognize speech from the microphone."""
    try:
        print("Listening...")
        audio = recognizer.listen(microphone, timeout=5, phrase_time_limit=5)
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
        return None
    except sr.WaitTimeoutError:
        print("No speech detected.")
        return None

def background_refresh(interval=3600):
    """
    Background thread to refresh the installed apps list periodically.
    """
    while True:
        time.sleep(interval)
        app_service.refresh_installed_apps()
        print("Installed apps list refreshed in the background.")

if __name__ == "__main__":
    # Initialize Jarvis
    speak("Initializing Jarvis")
    app_service.refresh_installed_apps()
    recognizer = sr.Recognizer()

    # Start background thread for periodic app list refresh
    threading.Thread(target=background_refresh, daemon=True).start()

    with sr.Microphone() as mic:
        # Calibrate the recognizer for ambient noise
        recognizer.adjust_for_ambient_noise(mic, duration=1)
        speak("Jarvis is ready. Say 'Jarvis' to wake up.")

        while True:
            # Listen for the wake word
            wake_word = recognize_speech(recognizer, mic)
            if wake_word and "jarvis" in wake_word.lower():
                speak("Yes sir, how can I help you?")

                # Ask for a command
                command = recognize_speech(recognizer, mic)

                if command:
                    process_command(command)
                else:
                    speak("I didn't hear a valid command. Please try again.")

            # Add a brief pause to avoid constant "no speech detected"
            print("Waiting for the next command...")
