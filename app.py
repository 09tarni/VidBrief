import streamlit as st

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="VidBrief",
    layout="centered",
)

# ==============================
# GLOBAL DARK THEME
# ==============================
st.markdown("""
<style>
html, body, [class*="css"] {
    background: radial-gradient(circle at top, #1e293b 0%, #020617 70%);
    color: #e5e7eb !important;
}

section.main > div {
    max-width: 900px;
    margin: auto;
}

/* Headings */
h1 {
    text-align: center;
    font-weight: 800;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 30px;
}

/* Card */
.card {
    background: #111827;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.45);
    margin-bottom: 25px;
}

/* Inputs */
input {
    background: #1f2937 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #374151 !important;
}

/* Buttons */
button {
    background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 12px 18px !important;
}

/* Summary blocks */
.summary-card {
    background: #1e293b;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 12px;
    border-left: 4px solid #8b5cf6;
}

.timestamp {
    color: #a78bfa;
    font-weight: 700;
}

/* Progress */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #7c3aed, #22d3ee);
}

/* Footer */
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 14px;
    margin: 60px 0 20px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("""
<div style="text-align:center;">
    <h1>🎬 VidBrief</h1>
    <p class="subtitle">
        Paste a YouTube link and generate a clean AI-powered summary
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE
# ==============================
for key in ["summary", "transcript", "error"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ==============================
# INPUT CARD
# ==============================
st.markdown("<div class='card'>", unsafe_allow_html=True)

with st.form("youtube_form"):
    youtube_url = st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=XXXX"
    )
    submit = st.form_submit_button("🚀 Generate Summary")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# PROCESS
# ==============================
if submit:
    if not youtube_url.strip():
        st.warning("Please enter a YouTube URL.")
    else:
        progress = st.progress(0)
        status = st.empty()

        try:
            from backend.utils.youtube_utils import clean_youtube_url
            from backend.downloader.youtube_downloader import download_audio
            from backend.transcription.whisper_transcriber import transcribe_audio
            from backend.summarization.text_summarizer import summarize_with_timestamps

            status.info("🔎 Cleaning YouTube URL...")
            clean_url = clean_youtube_url(youtube_url)
            progress.progress(15)

            status.info("📥 Downloading audio...")
            audio_path = download_audio(clean_url)
            progress.progress(40)

            status.info("🎙 Transcribing...")
            transcript, chunks = transcribe_audio(audio_path)
            progress.progress(70)

            status.info("🧠 Generating summary...")
            summary = summarize_with_timestamps(chunks)
            progress.progress(100)

            st.session_state.summary = summary
            st.session_state.transcript = transcript
            st.session_state.error = None

            status.success("✅ Summary generated successfully!")

        except Exception as e:
            st.session_state.error = str(e)
            status.error("❌ Something went wrong")

# ==============================
# ERROR
# ==============================
if st.session_state.error:
    st.error(st.session_state.error)

# ==============================
# OUTPUT
# ==============================
if st.session_state.summary:

    tab1, tab2 = st.tabs(["🧠 Summary", "📜 Transcript"])

    with tab1:
        view_mode = st.radio(
            "View style",
            ["Bullet points", "Paragraph"],
            horizontal=True
        )

        if view_mode == "Bullet points":
            for line in st.session_state.summary.split("\n"):
                if "—" in line:
                    ts, text = line.split("—", 1)
                    st.markdown(
                        f"<div class='summary-card'><span class='timestamp'>{ts}</span> — {text}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div class='summary-card'>{line}</div>",
                        unsafe_allow_html=True
                    )
        else:
            paragraph = " ".join(
                [line.split("—", 1)[-1].strip()
                 for line in st.session_state.summary.split("\n")]
            )
            st.markdown(
                f"<div class='summary-card' style='line-height:1.8'>{paragraph}</div>",
                unsafe_allow_html=True
            )

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇ Download Summary", st.session_state.summary)
        with col2:
            st.download_button("📋 Copy Summary", st.session_state.summary)

    with tab2:
        st.text_area("Transcript", st.session_state.transcript, height=420)

# ==============================
# FOOTER
# ==============================
st.markdown("""
<div class="footer">
    Built with Streamlit · Whisper · Transformers
</div>
""", unsafe_allow_html=True)
