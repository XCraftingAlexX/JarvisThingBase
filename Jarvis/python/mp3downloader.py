import os
import pytube
from moviepy.editor import *
import json

# Prompt the user to enter a YouTube video URL
url = input("Enter a YouTube video URL: ")

# Create a Pytube YouTube object
yt = pytube.YouTube(url)

# Get the audio stream
audio_stream = yt.streams.filter(only_audio=True).first()

# Set the path where the audio file will be saved
path = os.path.join("music", audio_stream.default_filename)

# Download the audio file
audio_file = audio_stream.download(output_path="music", filename="temp")

# Convert the audio file to mp3
mp3_file = path.split(".")[0] + ".mp3"
AudioFileClip(audio_file).write_audiofile(mp3_file)

# Remove temporary audio file
os.remove(audio_file)

print(f"MP3 file saved as {mp3_file}")

# Define the data to store in the JSON file
data = {"youtube_url": url, "mp3_file_name": mp3_file, "mp3_file_path": os.path.abspath(mp3_file)}

# Append the data to the JSON file
with open("music_data.json", "a") as f:
    json.dump(data, f)
    f.write("\n")