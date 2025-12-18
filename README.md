# 🎥 Multi-Modal Video Summarization System

## Overview
This project implements an end-to-end multi-modal video summarization pipeline that
automatically generates concise textual and visual summaries from video content.

The system integrates:
- Speech-to-Text (ASR)
- Transformer-based Text Summarization
- Visual Keyframe Extraction

## Pipeline
Video → Audio → Speech-to-Text → Text Summary  
Video → Frame Sampling → Keyframe Selection  

## Technologies Used
- Python
- OpenAI Whisper (ASR)
- HuggingFace Transformers (BART)
- OpenCV
- FFmpeg
- NumPy

## Key Features
- Robust handling of non-speech audio (no hallucinated transcripts)
- CPU-only execution (no GPU required)
- Modular pipeline design
- Multi-modal summarization (audio + visual)

## How to Run
1. Activate virtual environment
2. Run notebooks in order:
   - 01_audio_transcription.ipynb
   - 02_video_audio_transcription.ipynb
   - 03_text_summarization.ipynb
   - 04_keyframe_extraction.ipynb

## Results
- Generated speech transcripts from audio
- Produced concise summaries using Transformer models
- Extracted visually representative keyframes from video

## Future Improvements
- Summarization of longer videos
- Timestamp-aligned keyframe-text mapping
- Abstractive video summary generation
- Web interface for video upload
