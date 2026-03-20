import os
import random
import time
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from uploader import upload_video  # this is the uploader.py file we’ll create next

# Paths to your folders inside backend
MEDIA_DIR = "backend/media"
MUSIC_DIR = "backend/music"
CHANNELS_DIR = "backend/channels"

# Automatically get your channel JSON files
CHANNELS = os.listdir(CHANNELS_DIR)  # You should have 5 JSON files here

# Example topics for viral videos
TOPICS = ["space", "history", "psychology", "mystery", "science"]

# Function to create one video
def create_video(topic, index):
    # Pick a random image
    img_file = os.path.join(MEDIA_DIR, random.choice(os.listdir(MEDIA_DIR)))
    
    # Pick a random music file
    music_file = os.path.join(MUSIC_DIR, random.choice(os.listdir(MUSIC_DIR)))

    # Create a voice-over
    tts = gTTS(f"Did you know this about {topic}? Watch carefully!")
    voice_path = f"voice_{index}.mp3"
    tts.save(voice_path)

    # Load audio
    audio = AudioFileClip(voice_path)

    # Background image clip
    bg = ImageClip(img_file).set_duration(audio.duration)

    # Text overlay
    txt = TextClip(topic.upper(), fontsize=50, color="yellow", font="Arial-Bold") \
          .set_position("center").set_duration(audio.duration)

    # Combine background + text + audio
    video = CompositeVideoClip([bg, txt]).set_audio(audio)

    # Output file
    video_file = f"video_{topic}_{index}.mp4"
    video.write_videofile(video_file, fps=24, verbose=False, logger=None)

    # Clean up voice file
    os.remove(voice_path)

    return video_file

# Function to generate videos for all channels
def run_batch():
    for channel in CHANNELS:
        for i in range(5):  # 5 videos per channel
            topic = random.choice(TOPICS)
            print(f"Generating video {i+1} for {channel} on topic {topic}...")
            video_file = create_video(topic, i)

            # Upload video using uploader.py
            upload_video(video_file, os.path.join(CHANNELS_DIR, channel))

            # Random delay to prevent overload
            time.sleep(random.randint(300, 900))  # 5–15 minutes

# Run when script is executed
if __name__ == "__main__":
    run_batch()
