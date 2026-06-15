# AI Interview Coach with Speech Analysis

An intelligent AI-powered interview preparation tool with real-time speech feedback.

## Features
- Domain-specific questions (DSA, ML, Web Dev, HR)
- Voice recording + Whisper transcription
- LLM-powered feedback (content, structure, technical accuracy)
- Audio analysis (pace, filler words)
- Progress tracking with SQLite
- Sample answer comparison

## Setup
```bash
cd ai-interview-coach
pip install -r requirements.txt
streamlit run app.py
```

Add your LLM API key (Claude/Gemini) in the code for full analysis.

## Tech Stack
Python, Streamlit, Whisper, Librosa, SQLite