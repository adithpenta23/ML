import speech_recognition as sr
import pyttsx3
import groq
from config import grok_api_key
import os
from datetime import datetime

def ai(prompt):
    client = groq.Groq(api_key=grok_api_key)
    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_completion_tokens=600,
        top_p=0.95,
        reasoning_effort="default",
        stream=True,
        stop=None
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response

def say(text, engine):
    engine.say(text)
    engine.runAndWait()

def take_command(recog):
    with sr.Microphone() as source:
        print("Listening...")
        audio = recog.listen(source)
    print("Recognizing...")
    try:
        query = recog.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except Exception as e:
        print("Could not request results from Google Speech Recognition service.")
        return None

def save_conversation(log_path, speaker, text):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{speaker}: {text}\n")

if __name__ == "__main__":
    engine = pyttsx3.init()
    recog = sr.Recognizer()
    say("Hello, how can I assist you today?", engine)

    # Ensure prompts folder exists
    prompts_dir = os.path.join(os.path.dirname(__file__), "prompts")
    os.makedirs(prompts_dir, exist_ok=True)
    # Create a unique log file for this session
    log_filename = datetime.now().strftime("conversation_%Y%m%d_%H%M%S.txt")
    log_path = os.path.join(prompts_dir, log_filename)

    save_conversation(log_path, "AI", "Hello, how can I assist you today?")

    while True:
        query = take_command(recog)
        if not query:
            say("Sorry, I did not catch that. Please try again.", engine)
            save_conversation(log_path, "AI", "Sorry, I did not catch that. Please try again.")
            continue

        save_conversation(log_path, "User", query)

        if "exit" in query.lower() or "quit" in query.lower():
            say("Goodbye!", engine)
            save_conversation(log_path, "AI", "Goodbye!")
            break

        say("Let me think...", engine)
        response = ai(query)
        print(f"AI: {response}")
        save_conversation(log_path, "AI", response)
        say(response, engine)