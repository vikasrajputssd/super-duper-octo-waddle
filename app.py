import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, timedelta

# --- DB Setup ---
conn = sqlite3.connect('ladli_joo_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS japa_log (
            id INTEGER PRIMARY KEY,
            date TEXT,
            count INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS meditation_log (
            id INTEGER PRIMARY KEY,
            date TEXT,
            duration INTEGER)''')
conn.commit()

# --- App Config ---
st.set_page_config(page_title="Supreme Ladli Joo 2.0", layout='wide')

# --- CSS Styling ---
st.markdown("""
<style>
body {
    background-color: #fff8f0;
    font-family: 'Palatino Linotype', serif;
    color: #5a0b0b;
}
h1, h2 {
    color: #a10000;
    text-align: center;
    font-weight: 700;
}
.sidebar .sidebar-content {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/9/9b/Ladli_Joo_image_placeholder.jpg');
    background-size: cover;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar Menu ---
st.sidebar.title("🙏 श्री गुरुदेव एवं लाड़ली जू की कृपा से")
menu = st.sidebar.radio("मेनू चुनें:", ["नाम जप", "ध्यान", "भक्ति संदेश", "सेटिंग्स"])

# --- Helper Functions ---
def add_japa(count):
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT count FROM japa_log WHERE date = ?", (today,))
    row = c.fetchone()
    if row:
        new_count = row[0] + count
        c.execute("UPDATE japa_log SET count = ? WHERE date = ?", (new_count, today))
    else:
        c.execute("INSERT INTO japa_log (date, count) VALUES (?, ?)", (today, count))
    conn.commit()

def get_japa_data():
    c.execute("SELECT date, count FROM japa_log ORDER BY date DESC LIMIT 30")
    data = c.fetchall()
    df = pd.DataFrame(data, columns=['Date', 'Count'])
    if df.empty:
        df = pd.DataFrame({'Date': [], 'Count': []})
    return df

def add_meditation(duration):
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT duration FROM meditation_log WHERE date = ?", (today,))
    row = c.fetchone()
    if row:
        new_duration = row[0] + duration
        c.execute("UPDATE meditation_log SET duration = ? WHERE date = ?", (new_duration, today))
    else:
        c.execute("INSERT INTO meditation_log (date, duration) VALUES (?, ?)", (today, duration))
    conn.commit()

def get_meditation_data():
    c.execute("SELECT date, duration FROM meditation_log ORDER BY date DESC LIMIT 30")
    data = c.fetchall()
    df = pd.DataFrame(data, columns=['Date', 'Duration (min)'])
    if df.empty:
        df = pd.DataFrame({'Date': [], 'Duration (min)': []})
    return df

# --- Pages ---

if menu == "नाम जप":
    st.title("🔔 नाम जप पृष्ठ")
    st.markdown("**श्यामा-श्याम का नाम जप करें और अपनी भक्ति की गिनती बढ़ाएं।**")
    count = st.number_input("एक बार में कितने जप करना चाहते हैं?", min_value=1, max_value=108, value=1)
    if st.button("जप जोड़ें"):
        add_japa(count)
        st.success(f"आपके जप में {count} जप जोड़े गए। लाड़ली जू की कृपा बनी रहे!")
    
    df_japa = get_japa_data()
    if not df_japa.empty:
        fig = px.bar(df_japa, x='Date', y='Count', title="पिछले 30 दिनों के नाम जप", labels={"Count":"जप संख्या"})
        st.plotly_chart(fig)

elif menu == "ध्यान":
    st.title("🕉️ ध्यान पृष्ठ")
    duration = st.slider("ध्यान का समय (मिनट)", 1, 60, 10)
    if st.button("ध्यान शुरू करें"):
        st.info(f"ध्यान शुरू: {duration} मिनट")
        add_meditation(duration)
        # ध्यान टाइमर (सिंपल)
        for i in range(duration * 60, 0, -1):
            mins, secs = divmod(i, 60)
            st.markdown(f"<h1 style='text-align:center; color:#a10000;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
            time.sleep(1)
        st.success("ध्यान समाप्त हुआ! जय श्री राधा!")

    df_meditation = get_meditation_data()
    if not df_meditation.empty:
        fig = px.line(df_meditation, x='Date', y='Duration (min)', title="पिछले 30 दिनों का ध्यान समय")
        st.plotly_chart(fig)

elif menu == "भक्ति संदेश":
    st.title("🌸 भक्ति संदेश")
    st.markdown("""
    > "गुरुदेव और लाड़ली जू की कृपा से मन को शांति, जीवन को समृद्धि मिले।  
    > ध्यान और नाम जप के माध्यम से आत्मा को प्रबुद्ध करें।"
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Radha_Krishna_celebration_Vrindavan.jpg", use_column_width=True)

elif menu == "सेटिंग्स":
    st.title("⚙️ सेटिंग्स")
    st.markdown("यहां आप अपनी पसंद और ऐप के अन्य सेटिंग्स सेट कर सकते हैं।")
    # फ्यूचर सेटिंग्स के लिए जगह

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#a10000;'>© 2025 श्री गुरुदेव और लाड़ली जू की अनुकम्पा से | राधा माधव धाम, वृंदावन</p>",
    unsafe_allow_html=True
)

# --- बंद ---
conn.close()
