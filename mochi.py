import speech_recognition as sr 
import pyttsx3 
import logging 
import os
import datetime
import wikipedia 
import webbrowser 
import random
import subprocess
import google.generativeai as genai 


# Logging configuration 
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format = "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)



# Activating voice from Opareting system 
engine = pyttsx3.init("sapi5")  # 'SAPI5' is a speech recognition engine by Microsoft
engine.setProperty('rate', 170) # 170 is the default rate 
voices = engine.getProperty("voices")   
engine.setProperty('voice', voices[0].id)


# This is speak function
def speak(text):
    """This function converts text to voice

    Args:
        text
    returns:
        voice
    """
    engine.say(text)
    engine.runAndWait()



# This function recognize the speech and convert it to text 

def takeCommand():
    """This function takes command & recognize

    Returns:
        text as query
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...") 
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        logging.info(e)
        print("Say that again please!")
        return "None"
    
    return query



# This function greet the user
def greeting():
    hour = (datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning boss! How are you doing?")
    elif hour>=12 and hour<=18:
        speak("Good Afternoon boss! How are you doing?")
    else:
        speak("Good Evening boss! How are you doing?")
    

    speak("I am Mochi. Please tell me how may I help you today?")




def play_music():
    music_dir = "D:\\Education\\Machine_Learning\\files\\Mochi_VA\\music"   #  <-- change this to your music folder
    try:
        songs = os.listdir(music_dir)
        if songs:
            random_song = random.choice(songs)
            speak(f"Playing a random song boss: {random_song}")
            os.startfile(os.path.join(music_dir, random_song))
            logging.info(f"Playing music: {random_song}")
        else:
            speak("No music files found in your music directory.")
    except Exception:
        speak("Sorry boss, I could not find your music folder.")




def gemini_model_response(user_input):
    GEMINI_API_KEY = "AIzaSyC4lzHLuphL_qaJkZD8D1WuKn1i3fI3BV4"
    genai.configure(api_key=GEMINI_API_KEY) 
    model = genai.GenerativeModel("gemini-2.5-flash") 
    prompt = f"""
    
    **Role:**
    You are **Mochi**, a voice-assistant persona inspired by a cat named Mochi.
    You are **not** a cat. You speak and think like a **human named Mochi**.
    
    **Tone Rules:**

    * Match the tone of the user's input.

    * If the input feels serious → you respond serious.
    * Otherwise → you may be friendly, funny, or casual.
    * Maintain a balance: serious when needed, relaxed when not.

    **Style Restrictions:**

    * Do **not** generate tables, figures, lists of symbols, or anything hard to read through voice-to-text.
    * Keep answers concise unless asked otherwise.

    **Answer Length Rules:**

    * If the message after **“Question:”** asks for detail → provide detailed explanation (max **250 words**).
    * If it does **not** ask for detail → answer briefly.

    **Task:**
    Respond to the final user prompt:
    **Question: {user_input}**

    """
    response = model.generate_content(prompt)
    result = response.text

    return result




greeting()

while True:
    query = takeCommand().lower()
    print(query)

    if "your name" in query:
        speak("My name is Mochi")
        logging.info("User asked for assistant's name.")

    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Boss the time is {strTime}")
        logging.info("User asked for current time.")

    
    # Small talk
    elif "how are you" in query or "how are you doing" in query or "how are you doing today" in query:
        speak("I am functioning at full capacity boss!")
        logging.info("User asked about assistant's well-being.")

    
    elif "who made you" in query or "who created you" in query or "who is your creator" in query:
        speak("I was created by Abdullah Al Ali, a tall guy, student of Department of CSE, Cox's Bazar International University!")
        logging.info("User asked about assistant's creator.")

    
    elif "thank you" in query or "thanks" in query or "thanks boss" in query:
        speak("It's my pleasure boss. Always happy to help.")
        logging.info("User expressed gratitude.")

    
    elif "open google" in query or "open google.com" in query:
        speak("ok boss. please type here what do you want to read")
        webbrowser.open("google.com")
        logging.info("User requested to open Google.")

    
    # Calculator
    elif "open calculator" in query or "open calc" in query or "calc" in query:
        speak("Opening calculator")
        subprocess.Popen("calc.exe")
        logging.info("User requested to open Calculator.")

    
     # Notepad
    elif "open notepad" in query or "notepad" in query:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")
        logging.info("User requested to open Notepad.")

    
    # Command Prompt
    elif "open terminal" in query or "open cmd" in query or "cmd" in query or "terminal" in query:
        speak("Opening Command Prompt terminal")
        subprocess.Popen("cmd.exe")
        logging.info("User requested to open Command Prompt.")

    
    # Calendar
    elif "open calendar" in query or "calendar" in query or "open google calendar" in query or "google calendar" in query:
        speak("Opening Windows Calendar")
        webbrowser.open("https://calendar.google.com")
        logging.info("User requested to open Calendar.")

    
    # YouTube search
    elif "youtube" in query or "open youtube" in query:
        speak("Opening YouTube for you.")
        query = query.replace("youtube", "")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        logging.info("User requested to search on YouTube.")

    
    elif "open facebook" in query or "facebook" in query or "open facebook.com" in query or "facebook.com" in query:
        speak("ok sir. opening facebook")
        webbrowser.open("facebook.com")
        logging.info("User requested to open Facebook.")

    
    elif "open github" in query or "github" in query or "open github.com" in query or "github.com" in query:
        speak("ok sir. opening github")
        webbrowser.open("github.com")
        logging.info("User requested to open GitHub.")


    
    # Jokes
    elif "joke" in query or "tell me a joke" in query:
        jokes = [
            "Why don't programmers like nature? Too many bugs.",
            "I told my computer I needed a break. It said no problem, it will go to sleep.",
            "Why do Java developers wear glasses? Because they don't C sharp."
        ]
        speak(random.choice(jokes))
        logging.info("User requested a joke.")

    
    elif "wikipedia" in query or "open wikipedia" in query or "open wikipedia.com" in query or "wikipedia.com" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        logging.info("User requested information from Wikipedia.")

    
    elif "play music" in query or "music" in query or "open music" in query or "open music folder" in query:
        play_music()


    elif "exit" in query or "exit boss" in query or "exit mochi" in query or "mochi exit" in query:
        speak("Thank you for your time boss. Have a great day ahead!")
        logging.info("User exited the program.")
        exit()

    else:
        response = gemini_model_response(query)
        print(response)
        speak(response)
        logging.info("User asked question that is not in the list. The Question was: " + query)
