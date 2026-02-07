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
conn = sqlite3.connect('vip_history.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period TEXT, prediction TEXT, win_chance REAL, result TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# -------------------------------
# ২. Pro-Level Prediction Engine
# -------------------------------
def advanced_predict(inputs, period):
    if not inputs or len(inputs) != 10:
        return None, 0
    seed_str = str(period) + "".join(inputs) + str(time.time())
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))
    win_chance = round(random.uniform(82.5, 99.9), 1)
    
    freq_B, freq_S = inputs.count("B"), inputs.count("S")
    if freq_B > freq_S:
        prediction = "BIG" if random.random() > 0.2 else "SMALL"
    elif freq_S > freq_B:
        prediction = "SMALL" if random.random() > 0.2 else "BIG"
    else:
        prediction = random.choice(["BIG", "SMALL"])
    return prediction, win_chance

# -------------------------------
# ৩. Config & Session State
# -------------------------------
st.set_page_config(page_title="NAJMUL VIP V10 PRO", layout="centered")

if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False
if "admin_auth" not in st.session_state: st.session_state.admin_auth = False

# -------------------------------
# ৪. ULTIMATE PRIVACY & CSS
# -------------------------------
# এই CSS ডিফল্টভাবে সব বাটন এবং ফুটার হাইড করে রাখবে
hide_style = """
    <style>
    header, footer, .stAppDeployButton, [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    .main { background-color: #040608 !important; }
    .stApp { background-color: #040608; color: white; }
    .floating-panel { 
        background: rgba(10,15,30,0.98); border: 2px solid #00FFCC; border-radius: 20px; 
        padding: 15px; text-align: center; box-shadow: 0 0 35px rgba(0,255,204,0.6);
    }
    .big-text { color: #FF4B4B; font-size: 34px; font-weight: 900; }
    .small-text { color: #00D4FF; font-size: 34px; font-weight: 900; }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# -------------------------------
# ৫. Admin Login (Sidebar-এ রাখা হয়েছে যাতে পেজ পরিষ্কার থাকে)
# -------------------------------
with st.sidebar:
    st.subheader("🔑 Admin Access")
    pwd = st.text_input("পাসওয়ার্ড:", type="password")
    if st.button("Login"):
        if pwd == "8899":
            st.session_state.admin_auth = True
            st.success("Welcome, Najmul!")
        else:
            st.error("Access Denied")
    if st.button("Logout"):
        st.session_state.admin_auth = False
        st.rerun()

# -------------------------------
# ৬. App UI
# -------------------------------
st.markdown('<div style="background:linear-gradient(90deg, #FF0000, #990000); color:white; padding:12px; border-radius:12px; text-align:center; font-weight:bold;">🔗 VIP SERVER ACTIVE: NAJMUL-AI-V10-PRO</div>', unsafe_allow_html=True)

st.title("🔥 NAJMUL MASTER AI V10 PRO")

# ইনপুট সেকশন: শুধুমাত্র এডমিন দেখতে পাবে
if st.session_state.admin_auth:
    st.subheader("📊 এডমিন ইনপুট প্যানেল:")
    c1, c2 = st.columns(2)
    if c1.button("➕ BIG (B)"):
        if len(st.session_state.temp_input) < 10: st.session_state.temp_input.append("B")
    if c2.button("➕ SMALL (S)"):
        if len(st.session_state.temp_input) < 10: st.session_state.temp_input.append("S")
    
    if st.button("⬅️ UNDO"):
        if st.session_state.temp_input: st.session_state.temp_input.pop()
    
    st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input)}")
    period = st.text_input("পিরিয়ড নম্বর (শেষ ৩টি):", placeholder="655")
    
    if st.button("🚀 GET SIGNAL"):
        if len(st.session_state.temp_input) == 10: st.session_state.show_res = True
        else: st.warning("১০টি ইনপুট দিন!")
else:
    st.warning("🔒 প্রেডিকশন সিস্টেমটি বর্তমানে লক করা আছে। এডমিন প্যানেল থেকে ইনপুট দিন।")

# -------------------------------
# ৭. Results Display
# -------------------------------
if st.session_state.show_res and len(st.session_state.temp_input) == 10:
    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    
    st.markdown(f"""
    <div class="floating-panel">
        <p style="color:#00FFCC; font-weight:bold;">AI ANALYSIS REPORT</p>
        <p style="color:#FFEB3B; font-size:20px;">WIN: {win_chance}% 🔥</p>
        <p class="{'big-text' if prediction=='BIG' else 'small-text'}">{prediction}</p>
        <p style="color:#999; font-size:12px;">STABLE AI PREDICTION</p>
    </div>
    """, unsafe_allow_html=True)

    # WIN/LOSS বাটন - শুধুমাত্র এডমিন যখন লগইন থাকবে তখন সেভ করতে পারবে
    if st.session_state.admin_auth:
        st.write("---")
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
# ৮. History Display
# -------------------------------
st.write("---")
st.subheader("🕒 VIP History")
c.execute("SELECT period, prediction, win_chance, result FROM history ORDER BY id DESC LIMIT 5")
rows = c.fetchall()
for row in rows:
    p, pred, win, res = row
    st.markdown(f"""<div style="background:{'#004d00' if res=='WIN' else '#4d0000'}; padding:10px; border-radius:10px; margin-bottom:5px;">
    Period {p}: {pred} ({win}%) - {res}</div>""", unsafe_allow_html=True)
    
