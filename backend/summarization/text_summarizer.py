from transformers import pipeline

# Load model once
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)


def format_time(seconds: float) -> str:
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def group_segments(segments, window=60):
    """
    Groups whisper segments into time windows (seconds)
    """
    groups = []
    current = []
    start_time = 0

    for seg in segments:
        if not current:
            start_time = seg["start"]

        if seg["start"] - start_time <= window:
            current.append(seg)
        else:
            groups.append((start_time, current))
            current = [seg]
            start_time = seg["start"]

    if current:
        groups.append((start_time, current))

    return groups


def summarize_with_timestamps(segments):
    grouped = group_segments(segments, window=60)
    final_output = []

    for start_time, group in grouped:
        text_block = " ".join(seg["text"] for seg in group).strip()

        if len(text_block) < 40:
            continue

        summary = summarizer(
            text_block,
            max_length=60,
            min_length=25,
            do_sample=False
        )[0]["summary_text"]

        timestamp = format_time(start_time)
        final_output.append(f"{timestamp} — {summary}")

    return "\n".join(final_output)
