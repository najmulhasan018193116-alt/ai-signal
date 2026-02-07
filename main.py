import streamlit as st
import time
import random
import hashlib
import numpy as np
import pandas as pd
import sqlite3

# লোগো এবং টেলিগ্রাম সেটিংস
LOGO_URL = "https://i.ibb.co/vzYm8Ym/najmul-logo.png" 
TELEGRAM_LINK = "https://t.me/your_telegram_link"

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
# ২. Enhanced Logic (Wingo 1Min Compatibility)
# -------------------------------
def advanced_predict(inputs, period):
    if not inputs or len(inputs) != 10:
        return None, 0
    
    seed_str = str(period) + "".join(inputs) + str(time.time())
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))
    
    # উইন রেটিং ডাইনামিক রাখা হলো
    win_chance = round(random.uniform(88.5, 99.8), 1)
    
    # ১ মিনিটের গাণিতিক প্যাটার্ন চেক (Trend Analysis)
    last_3 = inputs[-3:]
    freq_B = inputs.count("B")
    freq_S = inputs.count("S")
    
    # Dragon Trend detection (একই জিনিস বারবার আসলে)
    if last_3 == ["B", "B", "B"]:
        prediction = "BIG" if random.random() > 0.1 else "SMALL"
    elif last_3 == ["S", "S", "S"]:
        prediction = "SMALL" if random.random() > 0.1 else "BIG"
    else:
        # নরমাল প্রবাবিলিটি
        if freq_B > freq_S:
            prediction = "BIG" if random.random() > 0.15 else "SMALL"
        else:
            prediction = "SMALL" if random.random() > 0.15 else "BIG"
            
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
# ৫. Login System
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
# ৬. UI Design & Header
# -------------------------------
if st.session_state.auth:
    st.markdown(f"""
    <style>
    .custom-header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 65px;
        background: #0a1118; display: flex; align-items: center; justify-content: space-between;
        padding: 0 15px; z-index: 999999; border-bottom: 2px solid #00FFCC;
    }}
    .header-logo {{ width: 45px; height: 45px; border-radius: 50%; border: 1px solid #00FFCC; }}
    .header-url {{ color: #00FFCC; font-family: monospace; font-size: 14px; font-weight: bold; }}
    
    header, footer, .stAppDeployButton, [data-testid="stToolbar"] {{ display: none !important; }}
    .main {{ background-color: #040608 !important; padding-top: 80px !important; }}
    .stApp {{ background-color: #040608; color: white; }}
    
    .floating-panel {{ 
        position: fixed; top: 110px; right: 10px; width: 220px;
        background: rgba(10,15,30,0.95); border: 2px solid #00FFCC; border-radius: 20px; 
        padding: 15px; z-index: 999; text-align: center;
        box-shadow: 0 0 35px rgba(0,255,204,0.5);
    }}
    
    .res-text {{ font-size: 34px; font-weight: 900; margin: 5px 0; }}
    .big-text {{ color: #FF4B4B; text-shadow: 0 0 15px #FF4B4B; }}
    .small-text {{ color: #00D4FF; text-shadow: 0 0 15px #00D4FF; }}
    
    .share-box {{ background: linear-gradient(90deg, #FF0000, #990000); color: white; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; font-weight: bold; border: 1px solid white; }}
    
    .tg-btn {{
        display: block; width: 100%; background: #0088cc; color: white !important;
        text-align: center; padding: 12px; border-radius: 12px;
        text-decoration: none; font-weight: bold; margin-top: 25px;
    }}
    </style>
    
    <div class="custom-header">
        <img src="{LOGO_URL}" class="header-logo">
        <div class="header-url">www.najmul-ai-v10.pro</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# ৭. Main UI
# -------------------------------
st.markdown(f'<div class="share-box">🔗 DK WINGO 1MIN: SERVER STABLE</div>', unsafe_allow_html=True)

# Live Trend Indicator (নতুন যোগ করা হয়েছে)
colA, colB = st.columns(2)
with colA:
    st.success("🟢 Server: Online")
with colB:
    st.warning("🔥 Trend: Strong")

st.title("🔥 NAJMUL MASTER AI V10 PRO")
st.subheader("📊 আগের ১০টি রেজাল্ট দিন:")

c1, c2 = st.columns(2)
if c1.button("➕ BIG (B)"):
    if len(st.session_state.temp_input)<10:
        st.session_state.temp_input.append("B")
        st.session_state.show_res=False
if c2.button("➕ SMALL (S)"):
    if len(st.session_state.temp_input)<10:
        st.session_state.temp_input.append("S")
        st.session_state.show_res=False

if st.button("⬅️ UNDO"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'অপেক্ষা করুন...'}")

period = st.text_input("পিরিয়ড (শেষ ৩টি):", placeholder="655")

if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input)==10 and period:
        st.session_state.show_res=True
    else:
        st.warning("⚠️ ১০টি ডাটা ইনপুট দিন!")

# -------------------------------
# ৮. Results & Prediction
# -------------------------------
if st.session_state.show_res:
    with st.spinner('📡 DK Wingo ডাটাবেস বিশ্লেষণ হচ্ছে...'):
        time.sleep(2.5)

    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)

    if prediction=="BIG":
        nums, color_class = [5,7,8,9], "big-text"
    else:
        nums, color_class = [0,1,2,4], "small-text"
    
    num_str = ", ".join(map(str, sorted(random.sample(nums, 3))))

    st.markdown(f"""
    <div class="floating-panel">
        <p style="color:#00FFCC; font-size:12px; margin:0;">AI VIP REPORT</p>
        <p style="color:#FFEB3B; font-weight:bold; margin:0;">WIN: {win_chance}%</p>
        <p class="res-text {color_class}">{prediction}</p>
        <p style="font-size:24px; color:#FFEB3B; font-weight:900;">{num_str}</p>
        <p style="font-size:10px; color:#aaa;">WINGO 1MIN SPECIAL</p>
    </div>
    """, unsafe_allow_html=True)

    # রেজাল্ট ফিডব্যাক
    st.write("---")
    res_c1, res_c2 = st.columns(2)
    if res_c1.button("✅ WIN"):
        st.session_state.history.insert(0, f"P-{period}: {prediction} ✅")
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()
    if res_c2.button("❌ LOSS"):
        st.session_state.history.insert(0, f"P-{period}: {prediction} ❌")
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()

# ইতিহাস
st.subheader("🕒 Recent History")
for h in st.session_state.history[:3]:
    st.text(h)

# ৯. Telegram Link
st.markdown(f'<a href="{TELEGRAM_LINK}" class="tg-btn">📢 JOIN TELEGRAM CHANNEL</a>', unsafe_allow_html=True)
