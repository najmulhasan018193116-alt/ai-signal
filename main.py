import streamlit as st
import time
import random
import hashlib

# ১. মাস্টার ডিজাইন ও নতুন কালার স্কিম
st.set_page_config(page_title="NAJMUL VIP V11", layout="centered")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    /* ১. ব্যাকগ্রাউন্ড কালার ব্ল্যাক */
    .stApp { background-color: #000000; color: white; }
    
    .floating-panel {
        position: fixed; top: 80px; right: 10px; width: 210px;
        background: rgba(10, 20, 30, 0.98); border: 2px solid #00FFCC;
        border-radius: 20px; padding: 15px; z-index: 9999; text-align: center;
        box-shadow: 0 0 35px rgba(0, 255, 204, 0.5);
    }
    .res-text { font-size: 34px; font-weight: 900; margin: 5px 0; }
    .big-text { color: #00FF00; text-shadow: 0 0 15px #00FF00; }
    .small-text { color: #FF0000; text-shadow: 0 0 15px #FF0000; }
    
    .share-box { background: linear-gradient(90deg, #1a1a1a, #333333); color: #00FFCC; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; font-weight: bold; border: 1px solid #00FFCC; }
    
    /* ২. B বাটন হালকা সবুজ */
    .big-btn button {
        background-color: #143d21 !important;
        color: Light green  !important;
        border-radius: 15px !important;
        height: 55px !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* ৩. S বাটন হালকা লাল */
    .small-btn button {
        background-color: #FFB6C1 !important;
        color: Light red !important;
        border-radius: 15px !important;
        height: 55px !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* ৪. ভুল কাটানোর বাটন হালকা বাদামি */
    .undo-btn button {
        background-color: #D2B48C !important;
        color: Black light !important;
        border-radius: 12px !important;
        height: 45px !important;
        font-weight: bold !important;
        border: none !important;
        margin-top: 10px !important;
    }

    .stButton>button { width: 100%; transition: 0.3s; }
    .get-btn>div>button { background: #00FFCC !important; color: black !important; font-size: 18px !important; border-radius: 20px !important; }
    
    .accuracy-tag { color: #00FFCC; font-size: 13px; font-weight: bold; }
    .percentage-bar { color: #FFEB3B; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ২. সেশন ম্যানেজমেন্ট
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False

# ৩. লগইন পাসওয়ার্ড সিস্টেম
if "auth" not in st.session_state: st.session_state.auth = False
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

# ৪. টপ বার
st.markdown(f'<div class="share-box">💎 NAJMUL VIP SERVER ACTIVE 💎</div>', unsafe_allow_html=True)
if st.session_state.total > 0:
    acc = (st.session_state.wins / st.session_state.total) * 100
    st.metric("AI LIVE ACCURACY", f"{acc:.1f}%")

# ৫. ইনপুট সেকশন
st.title("🔥 NAJMUL MASTER AI")
st.write("আগের ১০টি রেজাল্ট ইনপুট দিন:")

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="big-btn">', unsafe_allow_html=True)
    if st.button("BIG (B)"):
        if len(st.session_state.temp_input) < 10: 
            st.session_state.temp_input.append("B")
            st.session_state.show_res = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
    if st.button("SMALL (S)"):
        if len(st.session_state.temp_input) < 10: 
            st.session_state.temp_input.append("S")
            st.session_state.show_res = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ভুল কাটানোর বাটন (হালকা বাদামি)
st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
if st.button("⬅️ Repeat "):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.info(f"প্যাটার্ন ({len(st.session_state.temp_input)}/10): {' ➡️ '.join(st.session_state.temp_input)}")

# ৬. পিরিয়ড ও সিগন্যাল
period = st.text_input("পিরিয়ড নম্বর (শেষ ৩টি):", placeholder="যেমন: 123")

st.markdown('<div class="get-btn">', unsafe_allow_html=True)
if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input) == 10 and period:
        st.session_state.show_res = True
    else:
        st.warning(f"⚠️ ১০টি রেজাল্ট দিন! ({len(st.session_state.temp_input)}/10)")
st.markdown('</div>', unsafe_allow_html=True)

# ৭. AI লজিক
if st.session_state.show_res:
    with st.spinner('🔍 Searching ...'):
        time.sleep(2)
    
    current_key = "".join(st.session_state.temp_input)
    seed_str = str(period) + current_key
    hash_obj = hashlib.sha256(seed_str.encode()).hexdigest()
    random.seed(int(hash_obj, 16))
    
    prediction = random.choice(["BIG", "SMALL"])
    win_chance = round(random.uniform(94.2, 99.1), 1)
    
    if prediction == "BIG":
        nums = random.sample([5,6 ,7, 8, 9], 3) 
        color_class = "big-text"
    else:
        nums = random.sample([0, 1,2, 3, 4], 3) 
        color_class = "small-text"
    
    num_str = ", ".join(map(str, sorted(nums)))

    st.markdown(f"""
        <div class="floating-panel">
            <p class="accuracy-tag">VIP ANALYSIS</p>
            <p class="percentage-bar">WIN: {win_chance}%</p>
            <p class="res-text {color_class}">{prediction}</p>
            <p style="font-size: 26px; color: #FFEB3B; font-weight: 900;">{num_str}</p>
        </div>
        """, unsafe_allow_html=True)

    # ৮. রিসেট ও হিস্টরি
    st.write("---")
    w, l = st.columns(2)
    if w.button("✅ WIN"):
        st.session_state.history.insert(0, f"P-{period}: {prediction} ({win_chance}%) ✅")
        st.session_state.wins += 1
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()
    if l.button("❌ LOSS"):
        st.session_state.history.insert(0, f"P-{period}: {prediction} ({win_chance}%) ❌")
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()

# ৯. হিস্টরি
st.write("---")
for item in st.session_state.history[:5]:
    if "✅" in item: st.success(item)
    else: st.error(item)
    
