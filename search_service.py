import webbrowser as wb
import wikipedia

from tts_engine_service import speak

def search(query):
    """
    Search the query.
    """
    try:
        if "wiki" in query:
            query = query[5:].replace("on wikipedia", "").replace("on wiki", "").strip()
            data = info(query, 3, True)
            speak(data)
            return True

        else:
            query = query[6:].replace("on google", "").strip()
            speak(f"Searching for {query} on Google.")
            wb.open(f"https://www.google.com/search?q={query}")
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def info(topic: str, lines: int = 3, return_value: bool = False):
    """Gives Information on the Topic"""

    data = wikipedia.summary(topic, sentences = lines)
    print(data)
    if return_value:
        return data