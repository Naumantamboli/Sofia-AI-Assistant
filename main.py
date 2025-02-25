import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import pygetwindow as gw
import musicLibrary
import news
import requests
import google.generativeai as genai  # Import Gemini API

# Initialize Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice (Index 1)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_gemini(question):
    """Ask Gemini API and return response."""
    model = genai.GenerativeModel("gemini-pro")  # Use Gemini model
    response = model.generate_content(question)
    return response.text if response else "I don't have an answer for that."

def processCommand(c):
    c = c.strip().lower()  # Convert to lowercase properly
    print(c)  
    filename = ""

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:  
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif "open notepad" in c:
        os.system("notepad.exe")
        speak("Opened notepad")
    elif "open calculator" in c:
        os.system("calc.exe")
        speak("Opened calculator")
    elif "draw" in c:
        os.system("mspaint")
        speak("Draw now")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in the library.")
    elif "close browser" in c or "stop browser" in c:
        close_last_tab()
    elif "list files" in c:
        list_files()
    elif "create file" in c:
        filename = input("Enter the filename: ")
        create_file(filename)
    elif "delete file" in c:
        word = c.replace("delete file", "").strip()
        delete_file(word)
    elif "news" in c:
        web = "".join(c.split(" ")[1:])
        ans = news.list.get(web, None)
        if ans:
            webbrowser.open(ans)
        else:
            speak("No news found.")
    else:
        response = ask_gemini(c)  # Get response from Gemini AI
        speak(response)

def list_files():
    files = os.listdir()  # List all files in the current directory
    if files:
        speak("Here are the files in your directory:")
        for file in files:
            print(file)
            speak(file)
    else:
        speak("No files found.")

def create_file(filename):
    if filename:
        with open(filename, "w") as f:
            f.write("")
            speak("File created successfully")
    else:
        speak("Please give a filename correctly")

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        speak("Please give filename correctly")

def close_last_tab():
    chrome_windows = [win for win in gw.getWindowsWithTitle("Google Chrome")]
    
    if chrome_windows:
        chrome_windows[-1].close()  # Close the most recent Chrome window/tab
        speak("Closed the browser tab.")  
    else:
        speak("No Chrome window found.")

if __name__ == "__main__":
    speak("Initializing Sofia")
    while True:
        r = sr.Recognizer()
        print("Recognizing...")

        try:
            with sr.Microphone() as source:  # Initialize mic
                print("Listening..")
                audio = r.listen(source, timeout=5, phrase_time_limit=1)

            word = r.recognize_google(audio)
            if not word:  
                print("No speech detected.")
                continue  

            if word.lower() == "sofia":
                print(word.lower())
                speak("Yes Baby!")
                with sr.Microphone() as source:
                    print("Jo hukum..")
                    audio = r.listen(source, timeout=10)
                    command = r.recognize_google(audio)
                    processCommand(command.lower())

        except Exception as e:
            print(e)
