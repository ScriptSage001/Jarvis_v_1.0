import pyttsx3 as tts


def setup_voice():
    """Configures the voice settings to sound like Jarvis."""
    engine = tts.init()

    # Get available voices
    voices = engine.getProperty("voices")

    for voice in voices:
        if "MarkM" in voice.id:
            engine.setProperty("voice", voice.id)
            break

    # Adjust the rate (slightly slower for clarity like Jarvis)
    engine.setProperty("rate", 180)

    # Adjust the volume (1.0 is max)
    engine.setProperty("volume", 1.0)

    return engine

def speak(text):
    """Speak the given text."""
    engine = setup_voice()
    engine.say(text)
    engine.runAndWait()