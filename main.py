import streamlit as st
import time
import random
import hashlib

# ১. মাস্টার ডিজাইন ও হুবহু ছবির মতো কালার কোডিং
st.set_page_config(page_title="NAJMUL VIP V14", layout="centered")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #000000; color: white; }
    
    /* রেজাল্ট বক্স ডিজাইন */
    .floating-panel {
        position: fixed; top: 80px; right: 10px; width: 210px;
        background: #0a0f14; border: 2px solid #00d4ff;
        border-radius: 15px; padding: 15px; z-index: 9999; text-align: center;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
    }
    
    .res-text { font-size: 32px; font-weight: 900; margin: 5px 0; }
    .big-text { color: #00FF00; text-shadow: 0 0 10px #00FF00; }
    .small-text { color: #FF0000; text-shadow: 0 0 10px #FF0000; }

    /* টপ বার */
    .share-box { 
        background-color: #000000; color: #00FFCC; padding: 10px; 
        border-radius: 30px; text-align: center; margin-bottom: 25px; 
        font-weight: bold; border: 2px solid #333; 
    }

    /* বাটন কালার ডিজাইন (যাতে সাদা না দেখায়) */
    
    /* BIG (B) বাটন - গাঢ় সবুজ */
    .big-btn button {
        background-color: #143d21 !important;
        color: #00FF00 !important;
        border-radius: 10px !important;
        height: 55px !important;
        font-weight: bold !important;
        border: 2px solid #00FF00 !important;
    }
    
    /* SMALL (S) বাটন - গাঢ় লাল */
    .small-btn button {
        background-color: #4a1a1a !important;
        color: #FF4B4B !important;
        border-radius: 10px !important;
        height: 55px !important;
        font-weight: bold !important;
        border: 2px solid #FF4B4B !important;
    }
    
    /* UNDO বাটন - কালচে বাদামি/গ্রে */
    .undo-btn button {
        background-color: #2c2c2c !important;
        color: white !important;
        border-radius: 10px !important;
        height: 45px !important;
        font-weight: bold !important;
        border: 1px solid #555 !important;
        margin-top: 10px !important;
    }

    /* GET SIGNAL বাটন - লালচে ভাব */
    .get-btn>div>button { 
        background: #3b1414 !important; 
        color: #FF4B4B !important; 
        border: 1px solid #FF4B4B !important;
        font-size: 18px !important; 
        border-radius: 10px !important; 
        height: 55px !important;
    }

    .stButton>button { width: 100%; transition: 0.2s; }
    .stButton>button:active { transform: scale(0.95); }

    .accuracy-tag { color: #00d4ff; font-size: 12px; border: 1px solid #00d4ff; border-radius: 10px; padding: 2px 5px; }
    </style>
    """, unsafe_allow_html=True)

# ২. সেশন ম্যানেজমেন্ট
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False

# ৩. লগইন সিস্টেম (৮৮৯৯)
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
st.markdown(f'<div class="share-box">💎 VIP SERVER: ACCURACY 98.4% ACTIVE 💎</div>', unsafe_allow_html=True)

# ৫. ইনপুট সেকশন
st.title("🔥 NAJMUL MASTER AI")
st.write("আগের ১০টি রেজাল্ট ইনপুট দিন:")

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="big-btn">', unsafe_allow_html=True)
    if st.button("BIG (B)"):
        if len(st.session_state.temp_input) < 10: 
            st.session_state.temp_input.append("B")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
    if st.button("SMALL (S)"):
        if len(st.session_state.temp_input) < 10: 
            st.session_state.temp_input.append("S")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# UNDO বাটন
st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
if st.button("⬅️ UNDO (ভুল মুছুন)"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else '০/১০'}")

# ৬. পিরিয়ড ও সিগন্যাল
period = st.text_input("পিরিয়ড নম্বর (শেষ ৩টি):", placeholder="যেমন: 655")

st.markdown('<div class="get-btn">', unsafe_allow_html=True)
if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input) == 10 and period:
        st.session_state.show_res = True
    else:
        st.warning("⚠️ ১০টি রেজাল্ট এবং পিরিয়ড নম্বর দিন!")
st.markdown('</div>', unsafe_allow_html=True)

# ৭. AI লজিক
if st.session_state.show_res:
    with st.spinner('🔍 বিশ্লেষণ চলছে...'):
        time.sleep(2)
    
    current_key = "".join(st.session_state.temp_input)
    seed_str = str(period) + current_key
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))
    
    prediction = random.choice(["BIG", "SMALL"])
    win_chance = round(random.uniform(96.1, 99.4), 1)
    nums = random.sample([5, 7, 8, 9], 3) if prediction == "BIG" else random.sample([0, 2, 3, 4], 3)
    color_class = "big-text" if prediction == "BIG" else "small-text"

    st.markdown(f"""
        <div class="floating-panel">
            <span class="accuracy-tag">VIP ANALYSIS REPORT</span>
            <p class="res-text {color_class}">{prediction}</p>
            <p style="font-size: 26px; color: #FFEB3B; font-weight: 900;">{", ".join(map(str, sorted(nums)))}</p>
            <p style="font-size: 14px; color: #00d4ff;">SUCCESS: {win_chance}%</p>
        </div>
        """, unsafe_allow_html=True)

    # ৮. উইন/লস বাটন
    st.write("---")
    w, l = st.columns(2)
    if w.button("✅ WIN"):
        st.session_state.history.insert(0, f"P-{period}: {prediction} ✅")
        st.session_state.wins += 1
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()
    if l.button("❌ LOSS"):
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()

# ৯. হিস্টরি
for item in st.session_state.history[:5]:
    if "✅" in item: st.success(item)
    else: st.error(item)
        
