import sys
import threading
import tkinter as tk
import pydub
import speech_recognition
import pyttsx3 as tts
import time
import os
import json

from pydub import AudioSegment
from neuralintents import GenericAssistant
from pydub.playback import play


class Assistant:
    def __init__(self):
        # Initialize variables and GUI elements
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)

        self.assistant = GenericAssistant("intents.json", intent_methods={"file": self.create_file})
        self.assistant.load_model()

        self.root = tk.Tk()
        self.label = tk.Label(text="Speak", font=("Arial", 120, "bold"))
        self.label.pack()

        self.listen_event = threading.Event()
        self.command_event = threading.Event()

        self.current_audio = None
        self.stop_audio = False  # Flag to indicate when to stop audio
        self.stop_event = threading.Event()
        self.stop_play_thread = False  # Flag to indicate when to stop the play audio thread

        threading.Thread(target=self.run_assistant_thread).start()

        self.root.mainloop()

    def create_file(self):
        with open("somefile.txt", "w") as f:
            f.write("HELLO WORLD")
    
    def run_command_thread(self, text):
        self.command_event.set()

        if text == "stop":
            self.speaker.say("Stopping current command. Returning to listening mode.")
            self.speaker.runAndWait()
            self.command_event.clear()
            self.stop_audio = True  # set stop_audio flag to stop playing audio
            self.stop_event.set()
            while self.current_audio is not None and self.current_audio.is_playing():
                time.sleep(0.1)
            self.current_audio = None
        elif text == "it's time":
            audio_file = AudioSegment.from_file('music/fatherstretchmyhands.mp3')
            start_time = 29.79 * 1000
            end_time = 50 * 1000
            audio_file = audio_file[start_time:end_time].fade_in(1000).fade_out(1000)
            self.current_audio = audio_file
            self.stop_audio = False
            self.stop_event.clear()
            threading.Thread(target=self.play_audio_thread, args=(self.current_audio,)).start()
        elif "play" in text:
            with open("music.json") as f:
                audio_files = json.load(f)
            if audio_files:
                if "loop" in text:
                    self.stop_audio = False
                    self.stop_event.clear()
                    threading.Thread(target=self.play_loop_audio_thread, args=("music", audio_files)).start()
                else:
                    audio_file_path = os.path.join("music", audio_files[0])
                    audio_file = AudioSegment.from_file(audio_file_path)
                    self.current_audio = audio_file
                    self.stop_audio = False
                    self.stop_event.clear()
                    threading.Thread(target=self.play_audio_thread, args=(self.current_audio,)).start()
            else:
                self.speaker.say("Sorry, I couldn't find any audio files in the music folder.")
                self.speaker.runAndWait()
        else:
            if text is not None:
                response = self.assistant.request(text)
                if response is not None:
                    self.speaker.say(response)
                    self.speaker.runAndWait()

        self.command_event.clear()
        self.label.config(fg="black")

    def play_audio_thread(self, audio):
        self.stop_event.clear()
        self.stop_audio = False
        play_thread = threading.Thread(target=play, args=(audio,))
        play_thread.start()
        while not self.stop_event.is_set() and play_thread.is_alive() and not self.stop_audio:
            time.sleep(0.1)
        if play_thread.is_alive():
            play_thread.join()

    def play_loop_audio_thread(self, audio_folder, audio_files):
        self.stop_event.clear()
        self.stop_audio = False
        while self.command_event.is_set() and not self.stop_audio:
            for audio_file in audio_files:
                audio_file_path = os.path.join(audio_folder, audio_file)
                audio = AudioSegment.from_file(audio_file_path)
                self.current_audio = audio
                threading.Thread(target=self.play_audio_thread, args=(self.current_audio,)).start()
                time.sleep(audio.duration_seconds)


    def run_assistant_thread(self):
        while True:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                print("Speak now!")
                audio = self.recognizer.listen(mic)

            try:
                text = self.recognizer.recognize_google(audio)
                text = text.lower()
                print("You said: {}".format(text))

                if "assistant" in text and not self.listen_event.is_set():
                    self.label.config(fg="red")
                    self.speaker.runAndWait()
                    self.listen_event.set()

                elif self.listen_event.is_set():
                    self.listen_event.clear()

                    threading.Thread(target=self.run_command_thread, args=(text,)).start()

                # Check for stop_event flag and stop current audio if set to True
                if self.stop_event.is_set():
                    self.stop_event.clear()
                    self.stop_audio = True
                    self.current_audio.stop()

            except:
                self.label.config(fg="black")
                continue


Assistant()