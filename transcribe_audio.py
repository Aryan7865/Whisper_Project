import os
import whisper

# Cleanup previous segment files
for f in os.listdir():
    if f.startswith('segment_') and f.endswith(('.mp4', '.m4a', '.wav', '.ogg')):
        os.remove(f)

# Load Whisper model
model = whisper.load_model("base")

transcriptions = []

# List all files in the directory and filter by supported audio formats
supported_formats = [".mp4", ".m4a", ".wav", ".ogg"]
audio_files = [f for f in os.listdir() if any(f.lower().endswith(fmt) for fmt in supported_formats)]

# Transcribe and translate each audio file
for i, audio_file in enumerate(audio_files):
    print(f"Processing file {i+1}/{len(audio_files)}: {audio_file}")
    
    # Use Whisper to transcribe the audio and translate to English
    result = model.transcribe(audio_file, task="translate")
    translated_text = result['text']
    
    transcriptions.append(translated_text)

# Combine all transcriptions
full_transcription = " ".join(transcriptions)

# Save the full transcription to a file
with open("full_transcription.txt", "w") as f:
    f.write(full_transcription)

print("Transcription process completed.")
