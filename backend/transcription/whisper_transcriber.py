from faster_whisper import WhisperModel
import os

# Load model once
model = WhisperModel("small", device="cpu", compute_type="int8")

def transcribe_audio(audio_path):
    segments, info = model.transcribe(audio_path)

    full_text = ""
    chunk_results = []

    for seg in segments:
        text = seg.text.strip()
        full_text += text + " "

        chunk_results.append({
            "start": seg.start,
            "end": seg.end,
            "text": text
        })

    return full_text.strip(), chunk_results
