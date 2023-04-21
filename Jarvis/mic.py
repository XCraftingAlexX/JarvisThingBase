import speech_recognition as sr
import pyttsx3
import sys

r = sr.Recognizer()
engine = pyttsx3.init()

def recognize_and_speak():
    while True:

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            print("Speak now!")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: {}".format(text))
        
            engine.say(text)
            engine.runAndWait()
            
            if "exit" in text:
                sys.exit()

        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            
            engine.say("Sorry, I could not understand what you said.")
            engine.runAndWait()
        except sr.RequestError:
            print("Sorry, my speech service is currently unavailable.")
    
            engine.say("Sorry, my speech service is currently unavailable.")
            engine.runAndWait()

recognize_and_speak()
