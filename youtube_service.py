import webbrowser as web
import requests

from tts_engine_service import speak


def play_on_youtube(command):
    """
    Plays a song or artist playlist on YouTube based on the command.
    """
    search_query = command.lower().replace("play", "").replace("on youtube", "").strip()

    if search_query:
        speak(f"Searching for {search_query} on YouTube.")
        try:
            playonyt(search_query)  # Opens YouTube and plays the first result
        except Exception as e:
            speak(f"Sorry, I couldn't play {search_query} on YouTube.")
            print(f"Error: {e}")


def playonyt(topic: str, open_video: bool = True):
    """Play a YouTube Video"""

    url = f"https://www.youtube.com/results?q={topic}"
    count = 0
    cont = requests.get(url, timeout = 5)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == "WEB_PAGE_TYPE_WATCH":
            break
    if lst[count - 5] == "/results":
        raise Exception("No Video Found for this Topic!")

    if open_video:
        web.open(f"https://www.youtube.com{lst[count - 5]}")
    return f"https://www.youtube.com{lst[count - 5]}"