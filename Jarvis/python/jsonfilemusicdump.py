import json

# Read the data from the music.json file
with open('music.json', 'r') as f:
    music = json.load(f)

# Read the data from the music_data.json file
with open('music_data.json', 'r') as f:
    music_data = json.load(f)

# Extract the mp3_file_name from music_data
mp3_file_name = music_data['mp3_file_name']

# Check if mp3_file_name already exists in audio_files list
if mp3_file_name not in music['audio_files']:
    # Append the mp3_file_name to the audio_files list in music
    music['audio_files'].append(mp3_file_name)

# Write the updated data back to the music.json file
with open('music.json', 'w') as f:
    json.dump(music, f, indent=4)