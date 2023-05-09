import speech_recognition as sr
import pyttsx3
import multiprocessing as mp

# Set up the speech recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Global variables
command_executing = False
command_process = None

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get the command from the text
def get_command(text):
    if "what's the weather" in text.lower():
        return "get_weather"
    elif "what time is it" in text.lower():
        return "get_time"
    else:
        return None

# Function to execute the command
def execute_command(command):
    global command_executing
    if command == "get_weather":
        speak("The weather is sunny.")
    elif command == "get_time":
        speak("The time is 2:30 PM.")
    command_executing = False

# Function to listen for commands
def listen_for_commands():
    global command_executing, command_process
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: ", text)
            command = get_command(text)
            if command is None:
                speak("Sorry, I didn't understand that.")
            else:
                if command_process is not None and command_process.is_alive():
                    speak("Sorry, I am already busy.")
                else:
                    command_process = mp.Process(target=execute_command, args=(command,))
                    command_process.start()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            speak("Sorry, I am unable to process your request at this time.")

# Function to listen for the wake word
def listen_for_wake_word():
    global command_executing, command_process
    while True:
        with sr.Microphone() as source:
            print("Say the wake word!")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "test" in text.lower():
                speak("How can I help you?")
                # Stop the current command process if it's running
                if command_process is not None and command_process.is_alive():
                    command_process.terminate()
                break
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            continue

    # Listen for commands
    listen_for_commands()

# Start listening for the wake word
listen_for_wake_word()