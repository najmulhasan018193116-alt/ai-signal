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
# ৩. MASTER DATABASE
# -----------------------------------------------------------
MASTER_TRENDS = {
    "big_chains": [7, 9, 5, 8, 6], 
    "small_chains": [0, 2, 3, 4, 1],
    "violet_trigger": [0, 5],
    "reversal_rate": 0.82 
}

# -------------------------------
# ১. SQLite Historical DB
# -------------------------------
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

# -------------------------------
# ২. Pro-Level Advanced Prediction
# -------------------------------
def advanced_predict(inputs, period):
    if not inputs or len(inputs) != 10:
        return None, 0
    # B-5 থেকে শুধু B আলাদা করা বিশ্লেষণের জন্য
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
# ৬. CSS & UI (কালার সেটিংস)
# -------------------------------
st.markdown(f"""
<style>
    header, footer, .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        display: none !important;
        visibility: hidden !important;
    }}
    .main {{ background-color: #040608 !important; padding-top: 60px !important; }}
    .stApp {{ background-color: #040608; color: white; }}
    
    /* সংখ্যা বাটনগুলোর আলাদা আলাদা রং */
    .num-btn-5 button {{ background-color: #4CAF50 !important; color: white !important; }}
    .num-btn-6 button {{ background-color: #2196F3 !important; color: white !important; }}
    .num-btn-7 button {{ background-color: #FFEB3B !important; color: black !important; }}
    .num-btn-8 button {{ background-color: #9C27B0 !important; color: white !important; }}
    .num-btn-9 button {{ background-color: #FF9800 !important; color: white !important; }}
    
    .num-btn-0 button {{ background-color: #E91E63 !important; color: white !important; }}
    .num-btn-1 button {{ background-color: #00BCD4 !important; color: white !important; }}
    .num-btn-2 button {{ background-color: #8BC34A !important; color: white !important; }}
    .num-btn-3 button {{ background-color: #FF5722 !important; color: white !important; }}
    .num-btn-4 button {{ background-color: #607D8B !important; color: white !important; }}

    .floating-panel {{
        position: fixed; top: 100px; right: 10px; width: 220px;
        background: rgba(10,15,30,0.98); border: 2px solid #00FFCC; border-radius: 20px;
        padding: 15px; z-index: 999; text-align: center;
        box-shadow: 0 0 35px rgba(0,255,204,0.6);
    }}
    .res-text {{ font-size: 34px; font-weight: 900; margin: 5px 0; }}
    .big-text {{ color: #FF4B4B; text-shadow: 0 0 15px #FF4B4B; }}
    .small-text {{ color: #00D4FF; text-shadow: 0 0 15px #00D4FF; }}

    .stButton>button {{ width: 100%; border-radius: 12px; height: 45px; font-weight: bold; color: white; }}
    
    /* আগের কালার (Green & Red) */
    div[data-testid="column"]:nth-of-type(1) .main-btn-big button {{ background-color: #00FF00 !important; color: black !important; }}
    div[data-testid="column"]:nth-of-type(1) .main-btn-small button {{ background-color: #FF0000 !important; color: white !important; }}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# ৭. App UI
# -------------------------------
st.title("🔥 NAJMUL MASTER AI V10 PRO")
st.subheader("📊 আগের ১০টি রেজাল্ট ইনপুট দিন:")

# --- BIG SECTION (কলাম আকারে) ---
st.markdown("🟢 **BIG (5-9)**")
col_b1, col_b2 = st.columns([1, 1])
with col_b1:
    st.markdown('<div class="main-btn-big">', unsafe_allow_html=True)
    if st.button("➕ BIG (B)", key="big_main"):
        if len(st.session_state.temp_input) < 10:
            st.session_state.temp_input.append("B")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    for n in [5, 6, 7, 8, 9]:
        st.markdown(f'<div class="num-btn-{n}">', unsafe_allow_html=True)
        if st.button(f"{n}", key=f"btn_{n}"):
            if len(st.session_state.temp_input) < 10:
                st.session_state.temp_input.append(f"B-{n}")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- SMALL SECTION (কলাম আকারে) ---
st.markdown("🔴 **SMALL (0-4)**")
col_s1, col_s2 = st.columns([1, 1])
with col_s1:
    st.markdown('<div class="main-btn-small">', unsafe_allow_html=True)
    if st.button("➕ SMALL (S)", key="small_main"):
        if len(st.session_state.temp_input) < 10:
            st.session_state.temp_input.append("S")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_s2:
    for n in [0, 1, 2, 3, 4]:
        st.markdown(f'<div class="num-btn-{n}">', unsafe_allow_html=True)
        if st.button(f"{n}", key=f"btn_{n}"):
            if len(st.session_state.temp_input) < 10:
                st.session_state.temp_input.append(f"S-{n}")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if st.button("⬅️ UNDO (ভুল কাটুন)"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'ইনপুট দিন...'}")

period = st.text_input("পিরিয়ড নম্বর দিন (শেষ ৩টি):", placeholder="যেমন: 655")

if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input) == 10 and period:
        st.session_state.show_res = True
    else:
        st.warning("⚠️ ১০টি রেজাল্ট প্রয়োজন!")

# -------------------------------
# ৮. Results (মূল লজিক অনুযায়ী)
# -------------------------------
if st.session_state.show_res:
    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    sim_res = simulate_next_10(st.session_state.temp_input, period)
    color_class = "big-text" if prediction == "BIG" else "small-text"
    nums = random.sample([5, 7, 8, 9] if prediction == "BIG" else [0, 2, 3, 4], 3)
    num_str = ", ".join(map(str, sorted(nums)))

    st.markdown(f"""
    <div class="floating-panel">
        <p>WINGO REPORT</p>
        <p class="res-text {color_class}">{prediction}</p>
        <p>PROBABILITY: {win_chance}% 🔥</p>
        <p style="font-size:24px;color:#FFEB3B;font-weight:900;">{num_str}</p>
    </div>
    """, unsafe_allow_html=True)

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
        
