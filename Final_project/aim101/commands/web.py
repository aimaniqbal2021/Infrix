import webbrowser
import urllib.parse


def open_youtube():
    webbrowser.open("https://youtube.com")
    return "✅ Opening YouTube..."


def open_google():
    webbrowser.open("https://google.com")
    return "✅ Opening Google..."


def open_github():
    webbrowser.open("https://github.com")
    return "✅ Opening GitHub..."


def open_chatgpt():
    webbrowser.open("https://chat.openai.com")
    return "✅ Opening ChatGPT..."


def open_gmail():
    webbrowser.open("https://mail.google.com")
    return "✅ Opening Gmail..."


def open_facebook():
    webbrowser.open("https://facebook.com")
    return "✅ Opening Facebook..."


def search_google(query):
    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    webbrowser.open(url)
    return f"🔍 Searching Google for: {query}"


def search_youtube(query):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    webbrowser.open(url)
    return f"🎥 Searching YouTube for: {query}"