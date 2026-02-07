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
    freq_B = inputs.count("B")
    freq_S = inputs.count("S")
    base_prob_B = 50 + (freq_B - freq_S) * 5
    base_prob_B = max(10, min(90, base_prob_B))
    seed_str = str(period) + "".join(inputs)
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))
    win_chance = round(np.random.normal(base_prob_B, 4),1)
    win_chance = max(80, min(99.9, win_chance))
    prediction = "BIG" if random.random()*100 < win_chance else "SMALL"
    return prediction, win_chance

def simulate_next_10(inputs, period, runs=1000):
    results = {"BIG":0, "SMALL":0}
    for _ in range(runs):
        pred,_ = advanced_predict(inputs, period)
        results[pred] += 1
    return {k: round(v/runs*100,1) for k,v in results.items()}

# -------------------------------
# ৩. Streamlit Session + CSS
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
# ৬. Home Page CSS
# -------------------------------
if st.session_state.auth:
    st.markdown("""
    <style>
    html, body, .main { overflow: hidden !important; height: 100vh !important; }
    #MainMenu, header, footer { visibility: hidden; }
    .stApp { background-color: #040608; color: white; }
    .floating-panel { position: fixed; top: 80px; right: 10px; width: 220px;
        background: rgba(10,15,30,0.98); border: 2px solid #00FFCC; border-radius: 20px;
        padding: 15px; z-index: 9999; text-align: center;
        box-shadow: 0 0 35px rgba(0,255,204,0.6);}
    .res-text { font-size: 34px; font-weight: 900; margin: 5px 0; }
    .big-text { color: #FF4B4B; text-shadow: 0 0 15px #FF4B4B; }
    .small-text { color: #00D4FF; text-shadow: 0 0 15px #00D4FF; }
    .share-box { background: linear-gradient(90deg, #FF0000, #990000);
        color: white; padding: 12px; border-radius: 12px;
        text-align: center; margin-bottom: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------
# ৭. Top Bar
# -------------------------------
st.markdown('<div class="share-box">🔗 VIP SERVER ACTIVE: NAJMUL-AI-V10-PRO</div>', unsafe_allow_html=True)
if st.session_state.total > 0:
    acc = (st.session_state.wins / st.session_state.total) * 100
    st.metric("AI LIVE ACCURACY", f"{acc:.1f}%")

# -------------------------------
# ৮. Input Section
# -------------------------------
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

if st.button("⬅️ UNDO"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()

st.info(f"Pattern ({len(st.session_state.temp_input)}/10): {st.session_state.temp_input}")

# -------------------------------
# ৯. Period
# -------------------------------
period = st.text_input("Period (last 3 digits)")

if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input)==10 and period:
        st.session_state.show_res=True

# -------------------------------
# ১০. Result
# -------------------------------
if st.session_state.show_res:
    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    st.success(f"{prediction} | Win {win_chance}%")

# =====================================================
# 🔽🔽🔽 ADD-ON PART (ORIGINAL CODE UNCHANGED)
# =====================================================

st.write("---")
st.subheader("🧪 AUTO DEMO INPUT")

a,b = st.columns(2)

if a.button("⚡ AUTO RANDOM 10"):
    st.session_state.temp_input = [random.choice(["B","S"]) for _ in range(10)]
    st.session_state.show_res = False
    st.success("Auto Random Loaded")

if b.button("📌 LOAD DEMO PATTERN"):
    demo = ["B","B","S","B","S","B","S","B","B","S"]
    st.session_state.temp_input = demo.copy()
    st.session_state.show_res = False
    st.success("Demo Pattern Loaded")

st.write("---")
st.subheader("📈 Accuracy Breakdown (DB)")
try:
    df = pd.read_sql("SELECT result, COUNT(*) as total FROM history GROUP BY result", conn)
    st.dataframe(df)
except:
    st.info("No data yet")

st.write("---")
st.caption("⚠️ Educational & Demo Purpose Only. No real game/server accessed.")
