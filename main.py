from asyncio import timeout

import speech_recognition as sr
import webbrowser as wb
import pyttsx3 as tts
import music_library as ml

engine = tts.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    if "open google" in command.lower():
        wb.open("https://www.google.com")
    elif "open youtube" in command.lower():
        wb.open("https://www.youtube.com")
    elif "open facebook" in command.lower():
        wb.open("https://www.facebook.com")
    elif "open twitter" in command.lower():
        wb.open("https://www.twitter.com")
    elif "open instagram" in command.lower():
        wb.open("https://www.instagram.com")
    elif "open github" in command.lower():
        wb.open("https://www.github.com")
    elif "open linkedin" in command.lower():
        wb.open("https://www.linkedin.com")
    elif command.lower().startswith("play"):
        song = command[5:].lower()
        if song in ml.music.keys():
            speak(f"Playing {song}")
            wb.open(ml.music[song])
        else:
            speak(f"Sorry, I do not have {song} in my library")


if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using google
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout = 2, phrase_time_limit = 1)
            wake_word = r.recognize_google(audio)

            if wake_word.lower() == 'jarvis':
                speak("Yes sir, how can I help you?")

                with sr.Microphone() as source:
                    print("Listening...")
                    audio = r.listen(source)

                command = r.recognize_google(audio)
                process_command(command)

        except sr.UnknownValueError:
            print("Google could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google; {e}")
        except sr.WaitTimeoutError:
            print("No speech detected")

