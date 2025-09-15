import speech_recognition as sr
import pyttsx3
import webbrowser as wb
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
def take_command():
    recog=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=recog.listen(source)
    print("Recognizing...")
    try:
        query=recog.recognize_google(audio,language='en-in')
    except sr.UnknownValueError:
        return("Sorry, I could not understand the audio.")
    except Exception as e:
        return("Could not request results from Google Speech Recognition service.")
    return query
if __name__ == "__main__":
    say("Hello, how can I assist you today?")
    while True:
        query = take_command()
        sites=[["youtube","https://www.youtube.com"],["google","https://www.google.com"],["instagram","https://www.instagram.com"]]
        for site in sites:
            if site[0] in query.lower():
                wb.open(site[1])
                say(f"Opening {site[0]}")
                break
        else:
            if "exit" in query.lower() or "quit" in query.lower():
                say("Goodbye!")
                break
            else:
                say("Sorry, I can only open YouTube, Google, and Instagram. Please try again.")
