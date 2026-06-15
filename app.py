import streamlit as st
import sqlite3
import os
from datetime import datetime
import whisper
import librosa
import numpy as np
import soundfile as sf
from questions import get_question, get_sample_answer
from utils import count_filler_words, calculate_pace

# Initialize Whisper model
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

# Database setup
def init_db():
    conn = sqlite3.connect('interview_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (id INTEGER PRIMARY KEY, timestamp TEXT, domain TEXT, difficulty TEXT,
                  question TEXT, score REAL, pace REAL, fillers INTEGER)''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="AI Interview Coach", layout="wide")
st.title("🎤 AI Interview Coach with Speech Analysis")

# Sidebar
st.sidebar.header("Settings")
domain = st.sidebar.selectbox("Select Domain", ["DSA", "Machine Learning", "Web Development", "HR"])
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

if st.sidebar.button("Generate New Question"):
    question = get_question(domain, difficulty)
    st.session_state.question = question
    st.session_state.sample_answer = get_sample_answer(domain, question)

# Main area
if 'question' not in st.session_state:
    st.info("👈 Select domain & difficulty, then click 'Generate New Question'")
else:
    st.subheader("Interview Question:")
    st.write(st.session_state.question)

    # Audio Recorder
    st.subheader("Record Your Answer (30-60 seconds)")
    audio_file = st.audio_input("Record your response")

    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")

        if st.button("Analyze My Answer"):
            with st.spinner("Transcribing & Analyzing..."):
                # Save audio temporarily
                audio_path = "temp_audio.wav"
                with open(audio_path, "wb") as f:
                    f.write(audio_file.getbuffer())

                # Transcription
                result = model.transcribe(audio_path)
                transcription = result["text"]

                # LLM Analysis (placeholder - replace with Claude/Gemini)
                analysis = analyze_with_llm(transcription, st.session_state.question, domain)

                # Audio Analysis
                y, sr = librosa.load(audio_path)
                duration = librosa.get_duration(y=y, sr=sr)
                words = len(transcription.split())
                pace = calculate_pace(words, duration)
                fillers = count_filler_words(transcription)

                # Score
                total_score = (analysis['accuracy'] + analysis['structure'] + analysis['tech']) / 3

                # Save to DB
                save_session(domain, difficulty, st.session_state.question, total_score, pace, fillers)

                # Display Results
                display_scorecard(analysis, pace, fillers, transcription, st.session_state.sample_answer)

                os.remove(audio_path)

def analyze_with_llm(transcription, question, domain):
    # Placeholder - In real app, call Claude or Gemini API here
    return {
        'accuracy': 8,
        'structure': 7,
        'tech': 9,
        'suggestions': ["Improve STAR structure", "Add more specific examples"]
    }

def save_session(domain, difficulty, question, score, pace, fillers):
    conn = sqlite3.connect('interview_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO sessions VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
              (datetime.now().isoformat(), domain, difficulty, question, score, pace, fillers))
    conn.commit()
    conn.close()

def display_scorecard(analysis, pace, fillers, transcription, sample_answer):
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Overall Score", f"{(analysis['accuracy'] + analysis['structure'] + analysis['tech'])/3:.1f}/10")
        st.metric("Speaking Pace", f"{pace:.1f} words/min")
        st.metric("Filler Words", fillers)

    with col2:
        st.subheader("Feedback")
        for sug in analysis['suggestions']:
            st.write(f"• {sug}")

    st.subheader("Your Answer")
    st.write(transcription)

    st.subheader("Sample Good Answer")
    st.write(sample_answer)

# Progress page link in sidebar
st.sidebar.page_link("pages/1_Progress.py", label="View Progress")