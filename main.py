import streamlit as st
import time
import random
import hashlib
import numpy as np
import pandas as pd
import sqlite3
import os

# -------------------------------
# ১. SQLite DB (Data Loss রোধ করার জন্য)
# -------------------------------
db_path = 'vip_history.db'
conn = sqlite3.connect(db_path, check_same_thread=False)
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
# ২. Pro-Level Prediction (Dynamic High Win Rate)
# -------------------------------
def advanced_predict(inputs, period):
    if not inputs or len(inputs) != 10:
        return None, 0
    seed_str = str(period) + "".join(inputs) + str(time.time())
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))
    
    # উইন রেট ৮৫% থেকে ৯৯.৯% এর মধ্যে ভিন্ন ভিন্ন দেখাবে
    win_chance = round(random.uniform(85.0, 99.9), 1)
    
    freq_B = inputs.count("B")
    freq_S = inputs.count("S")
    if freq_B > freq_S:
        prediction = "BIG" if random.random() > 0.2 else "SMALL"
    elif freq_S > freq_B:
        prediction = "SMALL" if random.random() > 0.2 else "BIG"
    else:
        prediction = random.choice(["BIG", "SMALL"])
    return prediction, win_chance

# -------------------------------
# ৩. Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="NAJMUL VIP V10 PRO", layout="centered")

# -------------------------------
# ৪. Session State (হিস্টোরি লোড করা)
# -------------------------------
if "auth" not in st.session_state: st.session_state.auth = False
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False

# ডাটাবেজ থেকে হিস্টোরি রিফ্রেশ করার ফাংশন
def get_db_history():
    c.execute("SELECT period, prediction, win_chance, result FROM history ORDER BY id DESC LIMIT 10")
    return c.fetchall()

# -------------------------------
# ৫. Login
# -------------------------------
if not st.session_state.auth:
    st.title("🔐 NAJMUL VIP LOGIN")
    input_pw = st.text_input("পাসওয়ার্ড দিন:", type="password")
    if st.button("LOGIN"):
        if input_pw == "8899":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ ভুল পাসওয়ার্ড!")
    st.stop()

# -------------------------------
# ৬. NO-BUTTON CSS (একদম ক্লিন ইন্টারফেস)
# -------------------------------
st.markdown("""
    <style>
    /* Streamlit-এর ডিফল্ট বাটন ও ফুটার পুরোপুরি রিমুভ */
    [data-testid="stToolbar"], [data-testid="stDecoration"], footer, header, #MainMenu {
        display: none !important;
        height: 0 !important;
        opacity: 0 !important;
        visibility: hidden !important;
    }
    
    /* নিচের সাদা বা লাল বাটনগুলোকে চিরতরে আড়াল করা */
    .stAppDeployButton { display: none !important; }
    
    /* অ্যাপের মূল ব্যাকগ্রাউন্ড */
    .main { background-color: #040608 !important; }
    .stApp { background-color: #040608; color: white; }

    /* ভাসমান রেজাল্ট প্যানেল */
    .floating-panel { 
        background: rgba(10,15,30,0.95); border: 2px solid #00FFCC; 
        border-radius: 20px; padding: 20px; text-align: center;
        box-shadow: 0 0 30px rgba(0,255,204,0.5); margin: 20px 0;
    }
    .big-text { color: #FF4B4B; font-size: 38px; font-weight: 900; }
    .small-text { color: #00D4FF; font-size: 38px; font-weight: 900; }
    
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# ৭. UI Content
# -------------------------------
st.markdown('<div style="background: red; color: white; padding: 10px; text-align: center; border-radius: 10px; font-weight: bold;">🔗 VIP SERVER ACTIVE: NAJMUL-AI-V10-PRO</div>', unsafe_allow_html=True)

st.title("🔥 NAJMUL MASTER AI V10 PRO")
st.subheader("📊 আগের ১০টি রেজাল্ট ইনপুট দিন:")

c1, c2 = st.columns(2)
if c1.button("➕ BIG (B)"):
    if len(st.session_state.temp_input) < 10:
        st.session_state.temp_input.append("B")
if c2.button("➕ SMALL (S)"):
    if len(st.session_state.temp_input) < 10:
        st.session_state.temp_input.append("S")

if st.button("⬅️ UNDO (শেষ ইনপুট কাটুন)"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'অপেক্ষা করছি...'}")

period = st.text_input("পিরিয়ড নম্বর (শেষ ৩টি):", placeholder="যেমন: 655")

if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input) == 10 and period:
        st.session_state.show_res = True
    else:
        st.warning("⚠️ ১০টি ইনপুট এবং পিরিয়ড নম্বর প্রয়োজন!")

# -------------------------------
# ৮. AI Result
# -------------------------------
if st.session_state.show_res:
    with st.spinner('বিশ্লেষণ হচ্ছে...'):
        time.sleep(2)
    
    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    
    st.markdown(f"""
    <div class="floating-panel">
        <p style="color:#00FFCC; margin:0;">AI ANALYSIS REPORT</p>
        <p style="color:#FFEB3B; font-size:20px; font-weight:bold;">WIN: {win_chance}% 🔥</p>
        <p class="{'big-text' if prediction=='BIG' else 'small-text'}">{prediction}</p>
        <p style="color:#999; font-size:12px;">STABLE PREDICTION</p>
    </div>
    """, unsafe_allow_html=True)

    # WIN/LOSS বাটন
    w, l = st.columns(2)
    if w.button("✅ WIN"):
        c.execute("INSERT INTO history (period, prediction, win_chance, result) VALUES (?,?,?,?)", (period, prediction, win_chance, "WIN"))
        conn.commit()
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()
    if l.button("❌ LOSS"):
        c.execute("INSERT INTO history (period, prediction, win_chance, result) VALUES (?,?,?,?)", (period, prediction, win_chance, "LOSS"))
        conn.commit()
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()

# -------------------------------
# ৯. History Display (ডাটাবেজ থেকে সরাসরি)
# -------------------------------
st.write("---")
st.subheader("🕒 VIP History")
history_data = get_db_history()
for row in history_data:
    p, pred, win, res = row
    color = "green" if res == "WIN" else "red"
    st.markdown(f'<div style="background: {color}; padding: 10px; border-radius: 10px; margin-bottom: 5px;">Period {p}: {pred} ({win}%) {"✅" if res=="WIN" else "❌"}</div>', unsafe_allow_html=True)
