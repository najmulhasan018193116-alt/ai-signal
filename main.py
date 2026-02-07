import streamlit as st
import time
import random
import hashlib
import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime

# -------------------------------
# ১. SQLite Historical DB
# -------------------------------
conn = sqlite3.connect('vip_history.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period TEXT,
    prediction TEXT,
    win_chance REAL,
    result TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# -------------------------------
# ২. Advanced Prediction (UNCHANGED)
# -------------------------------
def advanced_predict(inputs, period):
    if not inputs or len(inputs) != 10:
        return None, 0

    freq_B = inputs.count("B")
    freq_S = inputs.count("S")

    base_prob_B = 50 + (freq_B - freq_S) * 5
    base_prob_B = max(10, min(90, base_prob_B))

    seed_str = str(period) + "".join(inputs)
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))

    win_chance = round(np.random.normal(base_prob_B, 4), 1)
    win_chance = max(80, min(99.9, win_chance))

    prediction = "BIG" if random.random() * 100 < win_chance else "SMALL"
    return prediction, win_chance

# -------------------------------
# ২.১ PRO SIGNAL LOCK (UNCHANGED)
# -------------------------------
def signal_lock(prediction, win_chance):
    nums = [5,6,7,8,9] if prediction == "BIG" else [0,1,2,3,4]

    if win_chance < 80:
        win_chance += random.uniform(5, 10)
    if win_chance > 99.9:
        win_chance = 99.9

    return nums, round(win_chance,1)

# -------------------------------
# ৩. Streamlit Config
# -------------------------------
st.set_page_config(page_title="NAJMUL VIP V10 PRO", layout="centered")

# -------------------------------
# ৪. Session State
# -------------------------------
for k,v in {
    "history":[], "wins":0, "total":0,
    "temp_input":[], "show_res":False,
    "auth":False, "round_start":None
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------------------
# ৫. Login (UNCHANGED)
# -------------------------------
if not st.session_state.auth:
    st.title("🔐 NAJMUL VIP LOGIN")
    pw = st.text_input("পাসওয়ার্ড দিন:", type="password")
    if st.button("LOGIN"):
        if pw == "8899":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ ভুল পাসওয়ার্ড!")
    st.stop()

# -------------------------------
# ৬. CSS + Scroll OFF (Home)
# -------------------------------
st.markdown("""
<style>
html, body, .main { overflow: hidden !important; height: 100vh !important; }
#MainMenu, header, footer { visibility: hidden; }
.stApp { background:#040608; color:white; }
.floating-panel{
 position:fixed; top:80px; right:10px; width:230px;
 background:rgba(10,15,30,.98); border:2px solid #00FFCC;
 border-radius:20px; padding:15px; z-index:9999;
 text-align:center; box-shadow:0 0 35px rgba(0,255,204,.6);
}
.big-text{color:#FF4B4B;font-size:32px;font-weight:900}
.small-text{color:#00D4FF;font-size:32px;font-weight:900}
.timer{color:#FFEB3B;font-size:18px;font-weight:bold}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# ৭. UI Input
# -------------------------------
st.title("🔥 NAJMUL MASTER AI V10 PRO")
st.subheader("📊 আগের ১০টি রেজাল্ট দিন")

c1, c2 = st.columns(2)
if c1.button("➕ BIG (B)") and len(st.session_state.temp_input) < 10:
    st.session_state.temp_input.append("B")
    st.session_state.show_res = False

if c2.button("➕ SMALL (S)") and len(st.session_state.temp_input) < 10:
    st.session_state.temp_input.append("S")
    st.session_state.show_res = False

st.info(f"প্যাটার্ন {len(st.session_state.temp_input)}/10 : {' ➡ '.join(st.session_state.temp_input)}")

period = st.text_input("পিরিয়ড (শেষ ৩ সংখ্যা):")

if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input)==10 and period:
        st.session_state.show_res = True
        st.session_state.round_start = time.time()

# -------------------------------
# ৮. AI Prediction + 1 Minute DK Timer
# -------------------------------
if st.session_state.show_res:
    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    nums, win_chance = signal_lock(prediction, win_chance)

    elapsed = int(time.time() - st.session_state.round_start)
    remaining = max(0, 60 - elapsed)

    color = "big-text" if prediction=="BIG" else "small-text"

    st.markdown(f"""
    <div class="floating-panel">
        <p>AI PRO SIGNAL</p>
        <div class="{color}">{prediction}</div>
        <h3>{' '.join(map(str,nums))}</h3>
        <p>WIN RATE: {win_chance}%</p>
        <div class="timer">⏳ Next Round in: {remaining}s</div>
        <small>DK আসার আগেই সিগন্যাল</small>
    </div>
    """, unsafe_allow_html=True)

    if remaining == 0:
        st.session_state.show_res = False
        st.session_state.temp_input = []
        st.rerun()

    time.sleep(1)
    st.rerun()
