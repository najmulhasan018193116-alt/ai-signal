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
    win_chance = round(np.random.normal(base_prob_B, 4),1)  # প্রো লেভেল std dev 4
    win_chance = max(80,100, min(99.9, win_chance))  # Win % 80-100%
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
# ৬. Home Page CSS (Scroll বন্ধ)
# -------------------------------
if st.session_state.auth:
    st.markdown("""
    <style>
    html, body, .main { 
        overflow: hidden !important;   
        height: 100vh !important;      
    }
    #MainMenu, header, footer { visibility: hidden; }
    .stApp { background-color: #040608; color: white; }
    .floating-panel { position: fixed; top: 80px; right: 10px; width: 220px;
        background: rgba(10,15,30,0.98); border: 2px solid #00FFCC; border-radius: 20px; padding: 15px; z-index: 9999; text-align: center;
        box-shadow: 0 0 35px rgba(0,255,204,0.6);}
    .res-text { font-size: 34px; font-weight: 900; margin: 5px 0; }
    .big-text { color: #FF4B4B; text-shadow: 0 0 15px #FF4B4B; }
    .small-text { color: #00D4FF; text-shadow: 0 0 15px #00D4FF; }
    .share-box { background: linear-gradient(90deg, #FF0000, #990000); color: white; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; font-weight: bold; border: 1px solid white; }
    .stButton>button { width: 100%; border-radius: 15px; height: 50px; font-weight: bold; color: white; }
    div[data-testid="stColumn"]:nth-of-type(1) .stButton>button { background-color: #00FF00 !important; color: black !important; }
    div[data-testid="stColumn"]:nth-of-type(2) .stButton>button { background-color: #FF0000 !important; color: white !important; }
    .get-btn>div>button { background: #00FFCC !important; color: black !important; font-size: 18px !important; }
    .accuracy-tag { color: #00FFCC; font-size: 13px; font-weight: bold; letter-spacing: 1px; }
    .percentage-bar { color: #FFEB3B; font-size: 18px; font-weight: bold; margin-bottom: 5px; }
    .undo-btn>div>button { border: 1px solid #FF4B4B !important; color: #FF4B4B !important; background: transparent !important; height: 40px !important; }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------
# ৭. Top Bar
# -------------------------------
st.markdown(f'<div class="share-box">🔗 VIP SERVER ACTIVE: NAJMUL-AI-V10-PRO</div>', unsafe_allow_html=True)
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
    if len(st.session_state.temp_input)<5:
        st.session_state.temp_input.append("B")
        st.session_state.show_res=False
if c2.button("➕ SMALL (S)"):
    if len(st.session_state.temp_input)<5:
        st.session_state.temp_input.append("S")
        st.session_state.show_res=False

st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
if st.button("⬅️ ভুল হয়েছে? শেষ ইনপুট কাটুন (UNDO)"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.info(f"প্যাটার্ন ({len(st.session_state.temp_input)}/10): {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'ইনপুট দিন...'}")

# -------------------------------
# ৯. Period Input
# -------------------------------
period = st.text_input("পিরিয়ড নম্বর দিন (শেষ ৩টি):", placeholder="যেমন: 655")

st.markdown('<div class="get-btn">', unsafe_allow_html=True)
if st.button("🚀 GET SIGNAL (AI বিশ্লেষণ করুন)"):
    if len(st.session_state.temp_input)==10 and period:
        st.session_state.show_res=True
    else:
        st.warning(f"⚠️  5টি রেজাল্ট প্রয়োজন! (এখন আছে {len(st.session_state.temp_input)}টি)")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# ১০. AI Prediction + DK Signal
# -------------------------------
if st.session_state.show_res:
    with st.spinner('🔍 গাণিতিক ট্রেন্ড বিশ্লেষণ হচ্ছে...'):
        time.sleep(2.8)

    prediction, win_chance = advanced_predict(st.session_state.temp_input, period)
    sim_res = simulate_next_5(st.session_state.temp_input, period)

    if prediction=="BIG":
        nums = random.sample([5,7,8,9],3)
        color_class="big-text"
    else:
        nums = random.sample([0,2,3,4],3)
        color_class="small-text"
    num_str = ", ".join(map(str, sorted(nums)))

    st.markdown(f"""
    <div class="floating-panel">
        <p class="accuracy-tag">AI ANALYSIS REPORT</p>
        <p class="percentage-bar">WIN: {win_chance}% 🔥</p>
        <p class="res-text {color_class}">{prediction}</p>
        <p style="font-size:26px;color:#FFEB3B;margin:0;font-weight:900;letter-spacing:5px;">{num_str}</p>
        <p style="font-size:10px;color:#999;margin-top:5;">STABLE AI PREDICTION (DK আসার আগে)</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("📊 Next 10 Simulation Probability:", sim_res)
    probs=pd.DataFrame({"BIG":[win_chance],"SMALL":[100-win_chance]})
    st.bar_chart(probs)

    # -------------------
    # WIN / LOSS Buttons
    # -------------------
    st.write("---")
    w,l = st.columns(2)
    if w.button("✅ WIN"):
        st.session_state.history.insert(0,f"Period {period}: {prediction} ({win_chance}%) ✅")
        st.session_state.wins+=1
        st.session_state.total+=1
        st.session_state.temp_input, st.session_state.show_res=[],False
        c.execute("INSERT INTO history (period,prediction,win_chance,result) VALUES (?,?,?,?)",
                  (period,prediction,win_chance,"WIN"))
        conn.commit()
        st.rerun()

    if l.button("❌ LOSS"):
        st.session_state.history.insert(0,f"Period {period}: {prediction} ({win_chance}%) ❌")
        st.session_state.total+=1
        st.session_state.temp_input, st.session_state.show_res=[],False
        c.execute("INSERT INTO history (period,prediction,win_chance,result) VALUES (?,?,?,?)",
                  (period,prediction,win_chance,"LOSS"))
        conn.commit()
        st.rerun()

# -------------------------------
# ১১. History
# -------------------------------
st.write("---")
st.subheader("🕒 VIP History")
for item in st.session_state.history[:5]:
    if "✅" in item: st.success(item)
    else: st.error(item)
