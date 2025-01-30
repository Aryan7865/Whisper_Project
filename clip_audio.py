# clip_audio.py
from pydub import AudioSegment

# Load your audio file
audio = AudioSegment.from_file("french.mp3")

# Clip the audio into 15-second segments
segment_length = 15000  # 15 seconds in milliseconds
segments = [audio[i:i+segment_length] for i in range(0, len(audio), segment_length)]

# Export segments
for i, segment in enumerate(segments):
    segment.export(f"segment_{i}.mp4", format="mp4")

