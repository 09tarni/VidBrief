import os
from pydub import AudioSegment


def split_audio(audio_path, chunk_length_ms=60000):
    os.makedirs("data/chunks", exist_ok=True)

    audio = AudioSegment.from_file(audio_path)
    chunks = []

    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = f"data/chunks/chunk_{i//chunk_length_ms}.wav"
        chunk.export(chunk_path, format="wav")

        chunks.append({
            "path": chunk_path,
            "start_sec": i // 1000
        })

    return chunks
