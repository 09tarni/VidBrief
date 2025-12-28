import os

# Root project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Data directories
DATA_DIR = os.path.join(BASE_DIR, "data")

AUDIO_DIR = os.path.join(DATA_DIR, "audio")
VIDEO_DIR = os.path.join(DATA_DIR, "videos")
TRANSCRIPT_DIR = os.path.join(DATA_DIR, "transcripts")
SUMMARY_DIR = os.path.join(DATA_DIR, "summaries")

# Keyframes directory
KEYFRAME_DIR = os.path.join(BASE_DIR, "keyframes")

# Ensure all folders exist
for path in [
    DATA_DIR,
    AUDIO_DIR,
    VIDEO_DIR,
    TRANSCRIPT_DIR,
    SUMMARY_DIR,
    KEYFRAME_DIR,
]:
    os.makedirs(path, exist_ok=True)
