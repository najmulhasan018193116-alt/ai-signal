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

# --- MASTER DATABASE (অপরিবর্তিত) ---
MASTER_TRENDS = {
    "big_chains": [7, 9, 5, 8, 6], 
    "small_chains": [0, 2, 3, 4, 1],
    "violet_trigger": [0, 5],
    "reversal_rate": 0.82 
}

# --- ১. SQLite Historical DB (অপরিবর্তিত) ---
conn = sqlite3.connect('vip_history.db', check_same_thread=False)
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

# --- ২. Pro-Level Advanced Prediction (অপরিবর্তিত) ---
def advanced_predict(inputs, period):
    if not inputs or len(inputs) != 10:
        return None, 0
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

# --- ৩. Streamlit Config ---
st.set_page_config(page_title="NAJMUL VIP V10 PRO", layout="centered")

# --- ৪. Session State (অপরিবর্তিত) ---
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False
if "auth" not in st.session_state: st.session_state.auth = False

# --- ৫. Login System ---
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

# --- ৬. CSS (রঙিন বাটন ও লেআউট) ---
st.markdown(f"""
<style>
    header, footer, .stAppDeployButton, [data-testid="stToolbar"] {{ display: none !important; }}
    .main {{ background-color: #040608 !important; padding-top: 50px !important; }}
    
    /* বাটন গুলোর জন্য আলাদা কালার */
    .stButton>button {{ width: 100% !important; border-radius: 8px !important; font-weight: bold; color: white; border: none; }}
    
    /* Row বাটন কালার সেটিংস */
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button {{ background-color: #4CAF50 !important; }} /* Green */
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button {{ background-color: #2196F3 !important; }} /* Blue */
    div[data-testid="stHorizontalBlock"] div:nth-child(3) button {{ background-color: #FFEB3B !important; color: black !important; }} /* Yellow */
    div[data-testid="stHorizontalBlock"] div:nth-child(4) button {{ background-color: #9C27B0 !important; }} /* Purple */
    div[data-testid="stHorizontalBlock"] div:nth-child(5) button {{ background-color: #FF9800 !important; }} /* Orange */

    .res-text {{ font-size: 34px; font-weight: 900; }}
</style>
""", unsafe_allow_html=True)

# --- ৭. UI Layout (সারি আকারে বাটন) ---
st.title("🔥 NAJMUL MASTER AI V10 PRO")

# BIG Row
st.markdown("🟢 **BIG (5-9)**")
b_cols = st.columns(5)
for i, n in enumerate([5, 6, 7, 8, 9]):
    if b_cols[i].button(f"{n}", key=f"btn_b_{n}"):
        if len(st.session_state.temp_input) < 10:
            st.session_state.temp_input.append(f"B-{n}")
            st.rerun()

# SMALL Row
st.markdown("🔴 **SMALL (0-4)**")
s_cols = st.columns(5)
for i, n in enumerate([0, 1, 2, 3, 4]):
    if s_cols[i].button(f"{n}", key=f"btn_s_{n}"):
        if len(st.session_state.temp_input) < 10:
            st.session_state.temp_input.append(f"S-{n}")
            st.rerun()

st.markdown("---")
# আপনার আগের BIG/SMALL বাটন
c1, c2 = st.columns(2)
if c1.button("➕ BIG (B)", type="primary"):
    if len(st.session_state.temp_input) < 10: st.session_state.temp_input.append("B"); st.rerun()
if c2.button("➕ SMALL (S)"):
    if len(st.session_state.temp_input) < 10: st.session_state.temp_input.append("S"); st.rerun()

if st.button("⬅️ UNDO"):
    if st.session_state.temp_input: st.session_state.temp_input.pop(); st.rerun()

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input)}")
period = st.text_input("পিরিয়ড নম্বর (শেষ ৩টি):", placeholder="যেমন: 655")

if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input) == 10 and period: st.session_state.show_res = True
    else: st.warning("⚠️ ১০টি রেজাল্ট প্রয়োজন!")

# --- ৮. Results (আপনার মূল কোড অনুযায়ী) ---
if st.session_state.show_res:
    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    st.markdown(f"### Result: {prediction} ({win_chance}%)")
    
    w, l = st.columns(2)
    if w.button("✅ WIN"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ✅")
        st.session_state.wins += 1
        st.session_state.total += 1
        c.execute("INSERT INTO history (period,prediction,win_chance,result) VALUES (?,?,?,?)", (period, prediction, win_chance, "WIN"))
        conn.commit()
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()
    if l.button("❌ LOSS"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ❌")
        st.session_state.total += 1
        c.execute("INSERT INTO history (period,prediction,win_chance,result) VALUES (?,?,?,?)", (period, prediction, win_chance, "LOSS"))
        conn.commit()
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()

st.subheader("🕒 VIP History")
for item in st.session_state.history[:5]:
    if "✅" in item: st.success(item)
    else: st.error(item)

st.markdown(f'<a href="{TELEGRAM_LINK}" target="_blank" style="display:block; background:#0088cc; color:white; text-align:center; padding:12px; border-radius:12px; text-decoration:none; font-weight:bold;">✈️ JOIN TELEGRAM</a>', unsafe_allow_html=True)
            
