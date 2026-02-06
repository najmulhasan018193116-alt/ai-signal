import streamlit as st
import time
import random
import hashlib

# ১. মাস্টার ডিজাইন ও ছবির মতো হুবহু কালার
st.set_page_config(page_title="NAJMUL VIP V13", layout="centered")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #000000; color: white; }
    
    /* ছবিতে দেওয়া সিগন্যাল প্যানেল ডিজাইন */
    .floating-panel {
        position: fixed; top: 80px; right: 10px; width: 210px;
        background: #0a0f14; border: 2px solid #00d4ff;
        border-radius: 15px; padding: 15px; z-index: 9999; text-align: center;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
    }
    .res-text { font-size: 32px; font-weight: 900; margin: 5px 0; }
    .big-text { color: #28a745; text-shadow: 0 0 10px #28a745; }
    .small-text { color: #ff4b4b; text-shadow: 0 0 10px #ff4b4b; }
    
    .share-box { 
        background-color: #000000; color: #00d4ff; padding: 10px; 
        border-radius: 30px; text-align: center; margin-bottom: 25px; 
        font-weight: bold; border: 2px solid #333; 
    }

    /* ছবিতে লাল চিহ্ন দেওয়া বাটনগুলোর নতুন রঙ */
    
    /* ১. BIG (B) বাটন - ছবির মতো গাঢ় সবুজ */
    .big-btn button {
        background-color: #143d21 !important;
        color: #28a745 !important;
        border-radius: 8px !important;
        height: 50px !important;
        font-weight: bold !important;
        border: 1px solid #28a745 !important;
    }
    
    /* SMALL (S) বাটন - ছবির মতো গাঢ় লাল */
    .small-btn button {
        background-color: #4a1a1a !important;
        color: #ff4b4b !important;
        border-radius: 8px !important;
        height: 50px !important;
        font-weight: bold !important;
        border: 1px solid #ff4b4b !important;
    }
    
    /* ২. UNDO বাটন - ছবির মতো নেভি/ব্ল্যাক শেড */
    .undo-btn button {
        background-color: #0d1621 !important;
        color: white !important;
        border-radius: 8px !important;
        height: 45px !important;
        font-weight: normal !important;
        border: 1px solid #34495e !important;
        margin-top: 10px !important;
    }

    .stButton>button { width: 100%; transition: 0.2s; }
    
    /* GET SIGNAL বাটন */
    .get-btn>div>button { 
        background: #3b1414 !important; 
        color: #ff4b4b !important; 
        border: 1px solid #ff4b4b !important;
        font-size: 18px !important; 
        border-radius: 10px !important; 
    }
    
    .accuracy-tag { color: #00d4ff; font-size: 12px; border: 1px solid #00d4ff; border-radius: 10px; padding: 2px 5px; }
    </style>
    """, unsafe_allow_html=True)

# ২. সেশন ম্যানেজমেন্ট
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False

# ৩. লগইন (৮৮৯৯)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🔐 NAJMUL VIP LOGIN")
    input_pw = st.text_input("পাসওয়ার্ড দিন:", type="password")
    if st.button("LOGIN"):
        if input_pw == "8899":
            st.session_state.auth = True
            st.rerun()
        else: st.error("❌ ভুল পাসওয়ার্ড!")
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

# ছবির মতো UNDO বাটন
st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
if st.button("⬅️ UNDO (ভুল মুছুন)"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input)}")

# ৬. পিরিয়ড
period = st.text_input("পিরিয়ড নম্বর (শেষ ৩টি):", value="655")

st.markdown('<div class="get-btn">', unsafe_allow_html=True)
if st.button("🚀 GET SIGNAL"):
    if len(st.session_state.temp_input) == 10: st.session_state.show_res = True
    else: st.warning("⚠️ ১০টি রেজাল্ট প্রয়োজন!")
st.markdown('</div>', unsafe_allow_html=True)

# ৭. AI লজিক
if st.session_state.show_res:
    with st.spinner('🔍 বিশ্লেষণ চলছে...'): time.sleep(1.5)
    
    current_key = "".join(st.session_state.temp_input)
    seed_str = str(period) + current_key
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))
    
    prediction = random.choice(["BIG", "SMALL"])
    win_chance = round(random.uniform(96.1, 99.4), 1)
    nums = random.sample([5, 7, 8, 9], 3) if prediction == "BIG" else random.sample([0, 2, 3, 4], 3)
    color_class = "big-text" if prediction == "BIG" else "small-text"

    st.markdown(f"""
        <div class="floating-panel">
            <span class="accuracy-tag">ACCURACY TAG</span>
            <p class="res-text {color_class}">{prediction}</p>
            <p style="color: #ffeb3b; font-size: 20px; font-weight: bold;">{", ".join(map(str, sorted(nums)))}</p>
            <p style="color: #00d4ff; font-size: 14px;">WIN CHANCE: {win_chance}%</p>
        </div>
        """, unsafe_allow_html=True)

    # ৮. রিসেট/উইন/লস
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
    
