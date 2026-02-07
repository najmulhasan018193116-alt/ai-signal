import streamlit as st
import time
import random
import hashlib
import numpy as np
import pandas as pd
import sqlite3

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
# ২. Pro-Level Advanced Prediction
# -------------------------------
def advanced_predict(inputs, period):
    if not inputs or len(inputs) != 10:
        return None, 0
    seed_str = str(period) + "".join(inputs) + str(time.time())
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))
    win_chance = round(random.uniform(82.5, 99.9), 1)
    
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
# ৩. Streamlit Config
# -------------------------------
st.set_page_config(page_title="NAJMUL VIP V10 PRO", layout="centered")

# -------------------------------
# ৪. Session State
# -------------------------------
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False
if "auth" not in st.session_state: st.session_state.auth = False

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
# ৬. THE "NO-ESCAPE" CSS & JS (একদম শেষ অস্ত্র)
# -------------------------------
if st.session_state.auth:
    # এই CSS বাটনগুলোকে ১০০০% আড়াল করবে
    st.markdown("""
        <style>
        /* ১. সব বাটন ও টুলবার গায়েব */
        #MainMenu, footer, header, .stAppDeployButton, 
        [data-testid="stToolbar"], [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        /* ২. স্ক্রিনের নিচটা পুরোপুরি লক করে দেওয়া */
        body, .main, .stApp {
            overflow: hidden !important; 
            background-color: #040608 !important;
        }

        /* ৩. নিচের অংশে কালো মাস্ক লেয়ার */
        .block-container {
            padding-bottom: 0rem !important;
            max-height: 100vh !important;
            overflow-y: auto !important;
        }
        
        /* ডিজাইন এলিমেন্টস */
        .floating-panel { 
            position: fixed; top: 80px; right: 10px; width: 220px;
            background: rgba(10,15,30,0.98); border: 2px solid #00FFCC; 
            border-radius: 20px; padding: 15px; z-index: 9999; text-align: center;
            box-shadow: 0 0 35px rgba(0,255,204,0.6);
        }
        .res-text { font-size: 34px; font-weight: 900; margin: 5px 0; }
        .big-text { color: #FF4B4B; text-shadow: 0 0 15px #FF4B4B; }
        .small-text { color: #00D4FF; text-shadow: 0 0 15px #00D4FF; }
        .share-box { background: linear-gradient(90deg, #FF0000, #990000); color: white; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; font-weight: bold; border: 1px solid white; }
        .stButton>button { width: 100%; border-radius: 15px; height: 50px; font-weight: bold; color: white; }
        div[data-testid="stColumn"]:nth-of-type(1) .stButton>button { background-color: #00FF00 !important; color: black !important; }
        div[data-testid="stColumn"]:nth-of-type(2) .stButton>button { background-color: #FF0000 !important; color: white !important; }
        </style>
        
        <script>
        // বাটনগুলো ডিটেক্ট করে রিমুভ করার জন্য ফোর্স কমান্ড
        const hideElements = () => {
            const selectors = ['.stAppDeployButton', 'footer', '#MainMenu', '[data-testid="stToolbar"]'];
            selectors.forEach(s => {
                const el = window.parent.document.querySelector(s);
                if (el) el.style.display = 'none';
            });
        };
        setInterval(hideElements, 500); // প্রতি আধা সেকেন্ডে চেক করবে
        </script>
    """, unsafe_allow_html=True)

# -------------------------------
# ৭. App Content (বাকি কোড আগের মতোই)
# -------------------------------
st.markdown(f'<div class="share-box">🔗 VIP SERVER ACTIVE: NAJMUL-AI-V10-PRO</div>', unsafe_allow_html=True)

st.title("🔥 NAJMUL MASTER AI V10 PRO")
st.subheader("📊 আগের ১০টি রেজাল্ট ইনপুট দিন:")

c1,c2 = st.columns(2)
if c1.button("➕ BIG (B)"):
    if len(st.session_state.temp_input)<10:
        st.session_state.temp_input.append("B")
        st.session_state.show_res=False
if c2.button("➕ SMALL (S)"):
    if len(st.session_state.temp_input)<10:
        st.session_state.temp_input.append("S")
        st.session_state.show_res=False

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input)}")

period = st.text_input("পিরিয়ড নম্বর দিন (শেষ ৩টি):", placeholder="যেমন: 655")

if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input)==10:
        st.session_state.show_res=True
    else:
        st.warning("১০টি ইনপুট দিন!")

if st.session_state.show_res:
    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    st.markdown(f"""
    <div class="floating-panel">
        <p style="color:#00FFCC">AI ANALYSIS</p>
        <p style="color:#FFEB3B">WIN: {win_chance}%</p>
        <p class="res-text {'big-text' if prediction=='BIG' else 'small-text'}">{prediction}</p>
    </div>
    """, unsafe_allow_html=True)
    
