import streamlit as st
import sqlite3
from datetime import datetime

# Initialize Database
conn = sqlite3.connect('ladli_joo_data.db', check_same_thread=False)
c = conn.cursor()

# Create tables
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS name_jap (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    count INTEGER,
                    timestamp TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS meditation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    duration INTEGER,
                    timestamp TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS bhajan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bhajan TEXT,
                    timestamp TEXT
                )''')
    conn.commit()

create_tables()

# Functions to add data
def add_name_jap(count):
    c.execute('INSERT INTO name_jap (count, timestamp) VALUES (?, ?)', (count, datetime.now()))
    conn.commit()

def add_meditation(duration):
    c.execute('INSERT INTO meditation (duration, timestamp) VALUES (?, ?)', (duration, datetime.now()))
    conn.commit()

def add_bhajan(bhajan):
    c.execute('INSERT INTO bhajan (bhajan, timestamp) VALUES (?, ?)', (bhajan, datetime.now()))
    conn.commit()

# Page setup
st.set_page_config(page_title="Ladli Joo Tracker", layout="centered")

st.title("🌸 लाड़ली जू की सेवा डायरी 🌸")
st.markdown("🙏 यह सेवा राधावल्लभ श्री हरिवंश नाम जप, ध्यान, और भजन के लिए है। 🙏")

st.markdown("---")

# Name Jap Section
st.header("📿 नाम जप")
count = st.number_input("जप की संख्या दर्ज करें (माला या नाम की गिनती):", min_value=1, step=1)
if st.button("जप दर्ज करें"):
    add_name_jap(count)
    st.success(f"🌼 {count} जप दर्ज किया गया! जय जय श्री राधे!")

# Meditation Section
st.header("🧘 ध्यान")
duration = st.slider("ध्यान की अवधि (मिनट में):", min_value=1, max_value=120, step=1)
if st.button("ध्यान शुरू करें"):
    add_meditation(duration)
    st.success(f"🕉️ {duration} मिनट ध्यान दर्ज किया गया! जय लाड़ली जू!")

# Bhajan Section
st.header("🎵 भजन")
bhajan_text = st.text_area("भजन लिखें (लाड़ली जू के भाव से):")
if st.button("भजन सहेजें"):
    if bhajan_text.strip():
        add_bhajan(bhajan_text)
        st.success("🎶 भजन सहेजा गया! आनंद भाव में रहो, लाड़ली जू तुम्हारी सेवा से प्रसन्न हैं।")
    else:
        st.warning("⚠️ कृपया भजन भरें।")

# Background Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #fff9f0;
            font-family: 'Noto Sans Devanagari', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)
