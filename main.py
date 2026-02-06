import streamlit as st
import time
import random
import hashlib

# ১. মাস্টার ডিজাইন
st.set_page_config(page_title="NAJMUL VIP V6", layout="centered")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #040608; color: white; }
    
    .floating-panel {
        position: fixed; top: 80px; right: 10px; width: 195px;
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
        if input_pw == "8899":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ ভুল পাসওয়ার্ড!")
    st.stop()

# ৪. টপ বার এবং একুরেসি স্ট্যাটাস
st.markdown(f'<div class="share-box">🔗 VIP SERVER ACTIVE: https://ai-signal-7w9ghbcvq7szvy5vuth2gw.streamlit.app</div>', unsafe_allow_html=True)
if st.session_state.total > 0:
    acc = (st.session_state.wins / st.session_state.total) * 100
    st.metric("AI LIVE ACCURACY", f"{acc:.1f}%")

# ৫. ইনপুট সেকশন (১০টি রেজাল্ট)
st.title("🔥 NAJMUL MASTER AI V6")
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

# বর্তমান প্যাটার্ন ভিউ
st.info(f"প্যাটার্ন ({len(st.session_state.temp_input)}/10): {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'ইনপুট দিন...'}")

# ৬. পিরিয়ড নম্বর ও সিগন্যাল বাটন
period = st.text_input("পিরিয়ড নম্বর দিন (শেষ ৩টি):", placeholder="যেমন: 655")

st.markdown('<div class="get-btn">', unsafe_allow_html=True)
if st.button("🚀 GET SIGNAL (AI বিশ্লেষণ করুন)"):
    if len(st.session_state.temp_input) == 10 and period:
        st.session_state.show_res = True
    else:
        st.warning(f"⚠️ ১০টি রেজাল্ট প্রয়োজন! (এখন আছে {len(st.session_state.temp_input)}টি)")

# ৭. প্রো-লেভেল AI লজিক
if st.session_state.show_res:
    with st.spinner('🔍 ১০-লেয়ার প্যাটার্ন বিশ্লেষণ করা হচ্ছে...'):
        time.sleep(2.5)
    
    current_key = "".join(st.session_state.temp_input)
    seed_str = str(period) + current_key
    random.seed(int(hashlib.sha256(seed_str.encode()).hexdigest(), 16))
    
    # এআই প্রেডিকশন
    prediction = random.choice(["BIG", "SMALL"])
    
    # নম্বর সিলেকশন (আপনার চার্ট অনুযায়ী)
    nums = random.sample([5,7,8,9], 3) if prediction == "BIG" else random.sample([0,1,2,4], 3)
    color_class = "big-text" if prediction == "BIG" else "small-text"
    num_str = ", ".join(map(str, sorted(nums)))

    st.markdown(f"""
        <div class="floating-panel">
            <p style="font-size: 11px; color: #00FFCC; margin:0; font-weight:bold;">ULTRA 10-LAYER AI</p>
            <p class="res-text {color_class}">{prediction}</p>
            <p style="font-size: 24px; color: white; margin:0; font-weight: 900;">{num_str}</p>
            <p style="font-size: 10px; color: #999; margin-top:5;">NAJMUL HACK V6</p>
        </div>
        """, unsafe_allow_html=True)

    # ৮. অটো-রিসেট ও হিস্টরি
    st.write("---")
    w, l = st.columns(2)
    if w.button("✅ WIN"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ✅")
        st.session_state.wins += 1
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()
    if l.button("❌ LOSS"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ❌")
        st.session_state.total += 1
        st.session_state.temp_input, st.session_state.show_res = [], False
        st.rerun()

# ৯. হিস্টরি
st.write("---")
st.subheader("🕒 VIP History")
for item in st.session_state.history[:5]:
    if "✅" in item: st.success(item)
    else: st.error(item)
    
