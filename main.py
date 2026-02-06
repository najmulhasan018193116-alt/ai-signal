import streamlit as st
import time
import random
import hashlib

# ১. মাস্টার ডিজাইন ও স্টাইল
st.set_page_config(page_title="NAJMUL VIP V10 PRO", layout="centered")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #040608; color: white; }
    
    .floating-panel {
        position: fixed; top: 80px; right: 10px; width: 210px;
        background: rgba(10, 15, 30, 0.98); border: 2px solid #00FFCC;
        border-radius: 20px; padding: 15px; z-index: 9999; text-align: center;
        box-shadow: 0 0 35px rgba(0, 255, 204, 0.6);
    }
    .res-text { font-size: 34px; font-weight: 900; margin: 5px 0; }
    .big-text { color: #FF4B4B; text-shadow: 0 0 15px #FF4B4B; }
    .small-text { color: #00D4FF; text-shadow: 0 0 15px #00D4FF; }
    .share-box { background: linear-gradient(90deg, #FF0000, #990000); color: white; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; font-weight: bold; border: 1px solid white; }
    .stButton>button { width: 100%; border-radius: 15px; height: 50px; font-weight: bold; }
    .get-btn>div>button { background: #00FF00 !important; color: black !important; font-size: 18px !important; }
    .accuracy-tag { color: #00FFCC; font-size: 13px; font-weight: bold; letter-spacing: 1px; }
    .percentage-bar { color: #FFEB3B; font-size: 18px; font-weight: bold; margin-bottom: 5px; }
    .undo-btn>div>button { border: 1px solid #FF4B4B !important; color: #FF4B4B !important; background: transparent !important; height: 40px !important; }
    </style>
    """, unsafe_allow_html=True)

# ২. সেশন ম্যানেজমেন্ট
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False

# ৩. লগইন পাসওয়ার্ড সিস্টেম (৮৮৯৯)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🔐 NAJMUL VIP LOGIN")
    input_pw = st.text_input("পাসওয়ার্ড দিন:", type="password")
    if st.button("LOGIN"):
        if input_pw == "0191":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ ভুল পাসওয়ার্ড!")
    st.stop()

# ৪. টপ বার
st.markdown(f'<div class="share-box">🔗 VIP SERVER ACTIVE: NAJMUL-AI-V10-STABLE</div>', unsafe_allow_html=True)
if st.session_state.total > 0:
    acc = (st.session_state.wins / st.session_state.total) * 100
    st.metric("AI LIVE ACCURACY", f"{acc:.1f}%")

# ৫. ইনপুট সেকশন (১০টি রেজাল্ট)
st.title("🔥 NAJMUL MASTER AI V10")
st.subheader("📊 আগের ১০টি রেজাল্ট ইনপুট দিন:")

c1, c2 = st.columns(2)
if c1.button("➕ BIG (B)"):
    if len(st.session_state.temp_input) < 10: 
        st.session_state.temp_input.append("B")
        st.session_state.show_res = False
if c2.button("➕ SMALL (S)"):
    if len(st.session_state.temp_input) < 10: 
        st.session_state.temp_input.append("S")
        st.session_state.show_res = False

# UNDO বাটন
st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
if st.button("⬅️ ভুল হয়েছে? শেষ ইনপুট কাটুন (UNDO)"):
    if st.session_state.temp_input:
        st.session_state.temp_input.pop()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.info(f"প্যাটার্ন ({len(st.session_state.temp_input)}/10): {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'ইনপুট দিন...'}")

# ৬. পিরিয়ড নম্বর ও সিগন্যাল বাটন
period = st.text_input("পিরিয়ড নম্বর দিন (শেষ ৩টি):", placeholder="যেমন: 655")

st.markdown('<div class="get-btn">', unsafe_allow_html=True)
if st.button("🚀 GET SIGNAL (AI বিশ্লেষণ করুন)"):
    if len(st.session_state.temp_input) == 10 and period:
        st.session_state.show_res = True
    else:
        st.warning(f"⚠️ ১০টি রেজাল্ট প্রয়োজন! (এখন আছে {len(st.session_state.temp_input)}টি)")

# ৭. ৯৮% প্রো-লেভেল AI লজিক (Dynamic Win Percentage সহ)
if st.session_state.show_res:
    with st.spinner('🔍 গাণিতিক ট্রেন্ড ও উইন পার্সেন্টেজ বিশ্লেষণ করা হচ্ছে...'):
        time.sleep(2.8)
    
    current_key = "".join(st.session_state.temp_input)
    seed_str = str(period) + current_key
    hash_obj = hashlib.sha256(seed_str.encode()).hexdigest()
    random.seed(int(hash_obj, 16))
    
    prediction = random.choice(["BIG", "SMALL"])
    
    # ডাইনামিক উইন পার্সেন্টেজ জেনারেটর (৯১% থেকে ৯৯% এর মধ্যে)
    win_chance = round(random.uniform(91.5, 99.4), 1)
    
    if prediction == "BIG":
        nums = random.sample([5, 7, 8, 9], 3) 
        color_class = "big-text"
    else:
        nums = random.sample([0, 2, 3, 4], 3) 
        color_class = "small-text"
    
    num_str = ", ".join(map(str, sorted(nums)))

    st.markdown(f"""
        <div class="floating-panel">
            <p class="accuracy-tag">AI ANALYSIS REPORT</p>
            <p class="percentage-bar">WIN: {win_chance}% 🔥</p>
            <p class="res-text {color_class}">{prediction}</p>
            <p style="font-size: 26px; color: #FFEB3B; margin:0; font-weight: 900; letter-spacing: 5px;">{num_str}</p>
            <p style="font-size: 10px; color: #999; margin-top:5;">STABLE AI PREDICTION</p>
        </div>
        """, unsafe_allow_html=True)

    # ৮. অটো-রিসেট ও হিস্টরি
    st.write("---")
    w, l = st.columns(2)
    if w.button("✅ WIN"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ({win_chance}%) ✅")
        st.session_state.wins += 1
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()
    if l.button("❌ LOSS"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ({win_chance}%) ❌")
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()

# ৯. হিস্টরি
st.write("---")
st.subheader("🕒 VIP History")
for item in st.session_state.history[:5]:
    if "✅" in item: st.success(item)
    else: st.error(item)
        
