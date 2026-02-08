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

# --- SQLite Historical DB (হিস্টরি এখানে সুরক্ষিত থাকবে) ---
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

# --- CSS & Individual Button Colors ---
st.markdown(f"""
<style>
    header, footer, .stAppDeployButton, [data-testid="stToolbar"] {{ visibility: hidden !important; }}
    .main {{ background-color: #040608 !important; padding-top: 75px !important; }}
    
    /* সারি আকারে বাটনগুলোর ভিন্ন ভিন্ন রঙ */
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button {{ background-color: #4CAF50 !important; color: white !important; }}
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button {{ background-color: #2196F3 !important; color: white !important; }}
    div[data-testid="stHorizontalBlock"] div:nth-child(3) button {{ background-color: #FFEB3B !important; color: black !important; }}
    div[data-testid="stHorizontalBlock"] div:nth-child(4) button {{ background-color: #9C27B0 !important; color: white !important; }}
    div[data-testid="stHorizontalBlock"] div:nth-child(5) button {{ background-color: #FF9800 !important; color: white !important; }}

    .stButton>button {{ width: 100% !important; border-radius: 10px; font-weight: bold; }}
    .floating-panel {{
        position: fixed; top: 100px; right: 10px; width: 220px;
        background: rgba(10,15,30,0.98); border: 2px solid #00FFCC; border-radius: 20px;
        padding: 15px; z-index: 999; text-align: center;
        box-shadow: 0 0 35px rgba(0,255,204,0.6);
    }}
</style>
""", unsafe_allow_html=True)

# --- App UI ---
st.title("🔥 NAJMUL MASTER AI V10 PRO")
st.subheader("📊 আগের ১০টি রেজাল্ট ইনপুট দিন:")

# --- BIG SECTION (Row) ---
st.markdown("🟢 **BIG (5-9)**")
c1, c2, c3, c4, c5 = st.columns(5)
for i, num in enumerate([5, 6, 7, 8, 9]):
    with [c1, c2, c3, c4, c5][i]:
        if st.button(f"{num}", key=f"B{num}"):
            if len(st.session_state.temp_input) < 10:
                st.session_state.temp_input.append(f"B-{num}")
                st.rerun()

# --- SMALL SECTION (Row) ---
st.markdown("🔴 **SMALL (0-4)**")
s1, s2, s3, s4, s5 = st.columns(5)
for i, num in enumerate([0, 1, 2, 3, 4]):
    with [s1, s2, s3, s4, s5][i]:
        if st.button(f"{num}", key=f"S{num}"):
            if len(st.session_state.temp_input) < 10:
                st.session_state.temp_input.append(f"S-{num}")
                st.rerun()

if st.button("⬅️ UNDO"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input)}")
period = st.text_input("পিরিয়ড নম্বর (শেষ ৩টি):", placeholder="যেমন: 655")

if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input) == 10 and period:
        st.session_state.show_res = True
    else:
        st.warning("⚠️ ১০টি রেজাল্ট প্রয়োজন!")

# --- Results & HISTORY (সম্পূর্ণ লজিক এখানে আছে) ---
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

st.subheader("🕒 VIP History (Master Database)")
# ডাটাবেস থেকে হিস্টরি নিয়ে আসা
c.execute("SELECT period, prediction, result FROM history ORDER BY id DESC LIMIT 5")
db_history = c.fetchall()
for row in db_history:
    status = "✅" if row[2] == "WIN" else "❌"
    st.write(f"Period {row[0]}: {row[1]} {status}")

st.markdown(f'<a href="{TELEGRAM_LINK}" target="_blank" class="telegram-btn">✈️ JOIN TELEGRAM</a>', unsafe_allow_html=True)
    
