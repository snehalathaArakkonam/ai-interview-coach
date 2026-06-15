import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.title("📈 Your Interview Progress")

conn = sqlite3.connect('../interview_history.db')
df = pd.read_sql_query("SELECT * FROM sessions ORDER BY timestamp DESC", conn)
conn.close()

if not df.empty:
    st.line_chart(df.set_index('timestamp')['score'])
    st.dataframe(df)
else:
    st.info("No sessions yet. Start practicing!")