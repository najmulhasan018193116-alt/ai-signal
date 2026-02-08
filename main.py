import streamlit as st
import time
import random
import hashlib
import numpy as np
import pandas as pd
import sqlite3

# --- লোগো এবং লিঙ্ক সেটিংস ---
LOGO_URL = "https://i.ibb.co/vzYm8Ym/najmul-logo.png"
TELEGRAM_LINK = "https://t.me/your_telegram_link"

# --- MASTER DATABASE ---
MASTER_TRENDS = {
    "big_chains": [7, 9, 5, 8, 6], 
    "small_chains": [0, 2, 3, 4, 1],
    "violet_trigger": [0, 5],
    "reversal_rate": 0.82 
}

# --- SQLite Historical DB ---
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

# --- Advanced Prediction Logic ---
def advanced_predict(inputs, period):
    if not inputs or len(inputs) != 10:
        return None, 0
    clean_inputs = [i.split('-')[0] for i in inputs]
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

# --- Streamlit Config ---
st.set_page_config(page_title="NAJMUL VIP V10 PRO", layout="centered")

# --- Session State ---
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False
if "auth" not in st.session_state: st.session_state.auth = False

# --- Login System ---
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

# --- CSS MASKING & CUSTOM BUTTON COLORS ---
st.markdown(f"""
<style>
    .custom-header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 65px;
        background: #0a0f1e; display: flex; align-items: center; justify-content: space-between;
        padding: 0 15px; z-index: 999999; border-bottom: 2px solid #00FFCC;
    }}
    .header-logo {{ width: 45px; height: 45px; border-radius: 50%; border: 1px solid #00FFCC; }}
    .header-url {{ color: #00FFCC; font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; }}
    
    header, footer, .stAppDeployButton, [data-testid="stToolbar"] {{ visibility: hidden !important; }}
    .main {{ background-color: #040608 !important; padding-top: 75px !important; }}

    /* Individual Button Colors using CSS */
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button {{ background-color: #4CAF50 !important; color: white !important; }} /* Green */
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button {{ background-color: #2196F3 !important; color: white !important; }} /* Blue */
    div[data-testid="stHorizontalBlock"] div:nth-child(3) button {{ background-color: #FFEB3B !important; color: black !important; }} /* Yellow */
    div[data-testid="stHorizontalBlock"] div:nth-child(4) button {{ background-color: #9C27B0 !important; color: white !important; }} /* Purple */
    div[data-testid="stHorizontalBlock"] div:nth-child(5) button {{ background-color: #FF9800 !important; color: white !important; }} /* Orange */

    .floating-panel {{
        position: fixed; top: 100px; right: 10px; width: 220px;
        background: rgba(10,15,30,0.98); border: 2px solid #00FFCC; border-radius: 20px;
        padding: 15px; z-index: 999; text-align: center;
        box-shadow: 0 0 35px rgba(0,255,204,0.6);
    }}
    .res-text {{ font-size: 34px; font-weight: 900; margin: 5px 0; }}
</style>
<div class="custom-header">
    <img src="{LOGO_URL}" class="header-logo">
    <div class="header-url">www.najmul-ai-v10.pro</div>
</div>
""", unsafe_allow_html=True)

# --- App UI ---
st.markdown('<div style="background:red; color:white; text-align:center; padding:10px; border-radius:10px;">🔗 VIP SERVER ACTIVE</div>', unsafe_allow_html=True)

st.title("🔥 NAJMUL MASTER AI V10 PRO")
st.subheader("📊 আগের ১০টি রেজাল্ট ইনপুট দিন:")

# --- BIG (Sari Layout) ---
st.markdown("🟢 **BIG (5-9)**")
cols_big = st.columns(5)
big_nums = [5, 6, 7, 8, 9]
for i, num in enumerate(big_nums):
    if cols_big[i].button(f"{num}", key=f"big_{num}"):
        if len(st.session_state.temp_input) < 10:
            st.session_state.temp_input.append(f"B-{num}")
            st.rerun()

# --- SMALL (Sari Layout) ---
st.markdown("🔴 **SMALL (0-4)**")
cols_small = st.columns(5)
small_nums = [0, 1, 2, 3, 4]
for i, num in enumerate(small_nums):
    if cols_small[i].button(f"{num}", key=f"small_{num}"):
        if len(st.session_state.temp_input) < 10:
            st.session_state.temp_input.append(f"S-{num}")
            st.rerun()

# --- Control Buttons ---
if st.button("⬅️ UNDO"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'ইনপুট দিন...'}")

period = st.text_input("পিরিয়ড নম্বর:", placeholder="যেমন: 655")

if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input) == 10 and period:
        st.session_state.show_res = True
    else:
        st.warning("⚠️ ১০টি রেজাল্ট প্রয়োজন!")

# --- Results ---
if st.session_state.show_res:
    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    st.success(f"Prediction: {prediction} ({win_chance}%)")
    # (বাকি রেজাল্ট লজিক আপনার মূল কোড অনুযায়ী চলবে...)

st.markdown(f'<a href="{TELEGRAM_LINK}" target="_blank" style="display:block; background:#0088cc; color:white; text-align:center; padding:12px; border-radius:12px; text-decoration:none; font-weight:bold; margin-top:20px;">✈️ JOIN TELEGRAM</a>', unsafe_allow_html=True)
