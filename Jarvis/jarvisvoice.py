import sys
import threading
import tkinter as tk
import pydub
import speech_recognition
import pyttsx3 as tts
import time
import os

from pydub import AudioSegment
from neuralintents import GenericAssistant
from pydub.playback import play
class Assistant:

    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)
        
        self.assistant = GenericAssistant("intents.json", intent_methods={"file": self.create_file})
        self.assistant.load_model()

        self.root = tk.Tk()
        self.label = tk.Label(text="Speak", font=("Arial", 120, "bold"))
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()
    
    def create_file(self):
        with open("somefile.txt", "w") as f:
            f.write("HELLO WORLD")

    def run_assistant(self):
        listening = False
        while True:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                print("Speak now!")
                audio = self.recognizer.listen(mic)
            try:
                text = self.recognizer.recognize_google(audio)
                text = text.lower()
                print("You said: {}".format(text))

                if "assistant" in text and not listening:
                    self.label.config(fg="red")
                    self.speaker.runAndWait
                    listening = True
                elif listening:
                    if text == "stop":
                        self.speaker.say("Bye")
                        self.speaker.runAndWait()
                        self.speaker.stop()
                        self.root.destroy()
                        listening = False
                        sys.exit()
                    elif text == "it's time":
                        audio_file = AudioSegment.from_file('music/fatherstretchmyhands.mp3')
                        start_time = 29.79 * 1000
                        end_time = 50 * 1000
                        audio_file = audio_file[start_time:end_time].fade_in(1000).fade_out(1000)
                        play(audio_file)
                        listening = False
                        self.label.config(fg="black")
                    elif "play" in text:
                        audio_folder = "music"
                        audio_files = [f for f in os.listdir(audio_folder) if f.endswith(".mp3")]
                        if audio_files:
                            if "loop" in text:
                                while True:
                                    for audio_file in audio_files:
                                        audio_file_path = os.path.join(audio_folder, audio_file)
                                        audio = AudioSegment.from_file(audio_file_path)
                                        play(audio)
                            else:
                                audio_file = AudioSegment.from_file(os.path.join(audio_folder, audio_files[0]))
                                play(audio_file)
                        else:
                            self.speaker.say("Sorry, I couldn't find any audio files in the music folder.")
                            self.speaker.runAndWait()
                        listening = False
                        self.label.config(fg="black")
                    else:
                        if text is not None:
                            response = self.assistant.request(text)
                            if response is not None:
                                self.speaker.say(response)
                                self.speaker.runAndWait()
                        self.label.config(fg="black")
                        listening = False
            except:
                self.label.config(fg="black")
                continue

                

Assistant()