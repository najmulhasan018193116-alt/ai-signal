import streamlit as st
import time
import random
import hashlib
import numpy as np
import pandas as pd
import sqlite3

# --- আপনার দেওয়া লোগো এবং লিঙ্ক সেটিংস ---
LOGO_URL = "https://i.ibb.co/vzYm8Ym/najmul-logo.png"
TELEGRAM_LINK = "https://t.me/your_telegram_link"

# -----------------------------------------------------------
# ৩. MASTER DATABASE (আপনার কোড - অপরিবর্তিত)
# -----------------------------------------------------------
MASTER_TRENDS = {
    "big_chains": [7, 9, 5, 8, 6], 
    "small_chains": [0, 2, 3, 4, 1],
    "violet_trigger": [0, 5],
    "reversal_rate": 0.82 
}

# -------------------------------
# ১. SQLite Historical DB (আপনার কোড - অপরিবর্তিত)
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
# ২. Pro-Level Advanced Prediction (আপনার কোড - অপরিবর্তিত)
# -------------------------------
def advanced_predict(inputs, period):
    if not inputs or len(inputs) != 10:
        return None, 0
    
    # ইনপুট থেকে B-5 থাকলে শুধু B আলাদা করা
    clean_inputs = [i.split('-')[0] if '-' in i else i for i in inputs]
    
    seed_str = str(period) + "".join(clean_inputs) + str(time.time())
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))
    win_chance = round(random.uniform(94.5, 99.8), 1)
    freq_B = clean_inputs.count("B")
    freq_S = clean_inputs.count("S")

    if clean_inputs[-3:] == ["B", "B", "B"]:
        prediction = "SMALL" if random.random() < MASTER_TRENDS["reversal_rate"] else "BIG"
    elif clean_inputs[-3:] == ["S", "S", "S"]:
        prediction = "BIG" if random.random() < MASTER_TRENDS["reversal_rate"] else "SMALL"
    elif freq_B > freq_S:
        prediction = "BIG" if random.random() > 0.10 else "SMALL"
    elif freq_S > freq_B:
        prediction = "SMALL" if random.random() > 0.10 else "BIG"
    else:
        prediction = random.choice(["BIG", "SMALL"])

    return prediction, win_chance

def simulate_next_10(inputs, period, runs=1000):
    results = {"BIG": 0, "SMALL": 0}
    for _ in range(runs):
        pred, _ = advanced_predict(inputs, period)
        results[pred] += 1
    return {k: round(v / runs * 100, 1) for k, v in results.items()}

# -------------------------------
# ৩. Streamlit Config
# -------------------------------
st.set_page_config(page_title="NAJMUL VIP V10 PRO", layout="centered")

# -------------------------------
# ৪. Session State (আপনার কোড - অপরিবর্তিত)
# -------------------------------
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False
if "auth" not in st.session_state: st.session_state.auth = False

# -------------------------------
# ৫. Login System (আপনার কোড - অপরিবর্তিত)
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
# ৬. CSS (আপনার অরিজিনাল স্টাইল + নতুন বাটন ডিজাইন)
# -------------------------------
if st.session_state.auth:
    st.markdown(f"""
    <style>
    .custom-header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 65px;
        background: #0a0f1e; display: flex; align-items: center; justify-content: space-between;
        padding: 0 15px; z-index: 999999; border-bottom: 2px solid #00FFCC;
    }}
    .header-logo {{ width: 45px; height: 45px; border-radius: 50%; border: 1px solid #00FFCC; }}
    .header-url {{ color: #00FFCC; font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; }}

    header, footer, .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        display: none !important;
        visibility: hidden !important;
    }}

    .main {{ background-color: #040608 !important; padding-top: 75px !important; }}
    .stApp {{ background-color: #040608; color: white; }}

    /* বাটন ডিজাইন */
    .stButton>button {{ width: 100%; border-radius: 8px; font-weight: bold; height: 45px; color: white; }}
    
    /* BIG/SMALL আগের কালার ঠিক রাখা */
    .big-main-btn button {{ background-color: #00e676 !important; color: black !important; }}
    .small-main-btn button {{ background-color: #ff1744 !important; color: white !important; }}
    
    /* সংখ্যা বাটনের ডিজাইন */
    .num-btn button {{ background-color: #222 !important; border: 1px solid #444 !important; height: 40px !important; }}
    
    .undo-btn-style button {{ background-color: #2c3e50 !important; color: white !important; height: 40px !important; }}
    .get-signal-btn button {{ background: linear-gradient(to right, #1e3c72, #2a5298) !important; font-size: 16px !important; height: 50px !important; }}

    .floating-panel {{
        position: fixed; top: 100px; right: 10px; width: 220px;
        background: rgba(10,15,30,0.98); border: 2px solid #00FFCC; border-radius: 20px;
        padding: 15px; z-index: 999; text-align: center;
        box-shadow: 0 0 35px rgba(0,255,204,0.6);
    }}
    .res-text {{ font-size: 34px; font-weight: 900; margin: 5px 0; }}
    .big-text {{ color: #FF4B4B; text-shadow: 0 0 15px #FF4B4B; }}
    .small-text {{ color: #00D4FF; text-shadow: 0 0 15px #00D4FF; }}
    .share-box {{ background: linear-gradient(90deg, #FF0000, #990000); color: white; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; font-weight: bold; border: 1px solid white; }}
    </style>

    <div class="custom-header">
        <img src="{LOGO_URL}" class="header-logo">
        <div class="header-url">www.najmul-ai-v10.pro</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# ৭. App UI (আপনার নতুন ডিজাইন অনুযায়ী)
# -------------------------------
st.markdown('<div class="share-box">🔗 VIP SERVER ACTIVE (SYCHRONIZED WITH MASTER DB)</div>', unsafe_allow_html=True)

st.title("🔥 NAJMUL MASTER AI V10 PRO")
st.subheader("📊 আগের ১০টি রেজাল্ট ইনপুট দিন:")

# --- BIG SECTION (আপনার HTML স্ট্রাকচার অনুযায়ী) ---
st.markdown('<div class="big-main-btn">', unsafe_allow_html=True)
if st.button("+ BIG (B)", key="b_main"):
    if len(st.session_state.temp_input) < 10:
        st.session_state.temp_input.append("B")
        st.session_state.show_res = False
st.markdown('</div>', unsafe_allow_html=True)

# B এর সংখ্যা সারি
cols_b = st.columns(5)
for i, num in enumerate([5, 6, 7, 8, 9]):
    with cols_b[i]:
        st.markdown('<div class="num-btn">', unsafe_allow_html=True)
        if st.button(str(num), key=f"b_n_{num}"):
            if len(st.session_state.temp_input) < 10:
                st.session_state.temp_input.append(f"B-{num}")
                st.session_state.show_res = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- SMALL SECTION (আপনার HTML স্ট্রাকচার অনুযায়ী) ---
st.markdown('<div class="small-main-btn">', unsafe_allow_html=True)
if st.button("+ SMALL (S)", key="s_main"):
    if len(st.session_state.temp_input) < 10:
        st.session_state.temp_input.append("S")
        st.session_state.show_res = False
st.markdown('</div>', unsafe_allow_html=True)

# S এর সংখ্যা সারি
cols_s = st.columns(5)
for i, num in enumerate([0, 1, 2, 3, 4]):
    with cols_s[i]:
        st.markdown('<div class="num-btn">', unsafe_allow_html=True)
        if st.button(str(num), key=f"s_n_{num}"):
            if len(st.session_state.temp_input) < 10:
                st.session_state.temp_input.append(f"S-{num}")
                st.session_state.show_res = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# UNDO বাটন
st.markdown('<div class="undo-btn-style">', unsafe_allow_html=True)
if st.button("⬅ ভুল হয়েছে? শেষ ইনপুট কাটুন (UNDO)"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# প্যাটার্ন ডিসপ্লে
st.info(f"প্যাটার্ন ({len(st.session_state.temp_input)}/10): {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'ইনপুট দিন...'}")

# পিরিয়ড ইনপুট
period = st.text_input("পিরিয়ড নম্বর দিন (শেষ ৩টি):", placeholder="যেমন: 655")

# সিগন্যাল বাটন
st.markdown('<div class="get-signal-btn">', unsafe_allow_html=True)
if st.button("🚀 GET SIGNAL (AI বিশ্লেষণ করুন)"):
    if len(st.session_state.temp_input) == 10 and period:
        st.session_state.show_res = True
    else:
        st.warning("⚠️ ১০টি রেজাল্ট প্রয়োজন!")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# ৮. Results (আপনার অরিজিনাল কোড অনুযায়ী)
# -------------------------------
if st.session_state.show_res:
    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    sim_res = simulate_next_10(st.session_state.temp_input, period)

    color_class = "big-text" if prediction == "BIG" else "small-text"
    nums = random.sample([5, 7, 8, 9] if prediction == "BIG" else [0, 2, 3, 4], 3)
    num_str = ", ".join(map(str, sorted(nums)))

    st.markdown(f"""
    <div class="floating-panel">
        <p>WINGO MASTER REPORT</p>
        <p>PROBABILITY: {win_chance}% 🔥</p>
        <p class="res-text {color_class}">{prediction}</p>
        <p style="font-size:26px;color:#FFEB3B;font-weight:900;">{num_str}</p>
    </div>
    """, unsafe_allow_html=True)

    w, l = st.columns(2)
    if w.button("✅ WIN"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ✅")
        st.session_state.wins += 1
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        c.execute("INSERT INTO history (period,prediction,win_chance,result) VALUES (?,?,?,?)", (period, prediction, win_chance, "WIN"))
        conn.commit()
        st.rerun()

    if l.button("❌ LOSS"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ❌")
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        c.execute("INSERT INTO history (period,prediction,win_chance,result) VALUES (?,?,?,?)", (period, prediction, win_chance, "LOSS"))
        conn.commit()
        st.rerun()

st.write("---")
st.subheader("🕒 VIP History")
for item in st.session_state.history[:5]:
    if "✅" in item: st.success(item)
    else: st.error(item)

st.markdown(f'<a href="{TELEGRAM_LINK}" target="_blank" class="telegram-btn">✈️ JOIN OUR TELEGRAM</a>', unsafe_allow_html=True)
    
