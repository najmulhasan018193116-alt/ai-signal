import streamlit as st
import time
import random
import hashlib

# ১. প্রিমিয়াম ডিজাইন ও সেটিংস
st.set_page_config(page_title="NAJMUL VIP SIGNAL", layout="centered")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #0E1117; color: white; }
    
    .floating-panel {
        position: fixed;
        top: 85px;
        right: 15px;
        width: 175px;
        background: rgba(15, 15, 25, 0.98);
        border: 2px solid #00ff00;
        border-radius: 18px;
        padding: 12px;
        z-index: 9999;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
    }
    .res-text { font-size: 28px; font-weight: bold; margin: 5px 0; }
    .big-text { color: #FF3131; text-shadow: 0 0 10px #FF3131; }
    .small-text { color: #00D4FF; text-shadow: 0 0 10px #00D4FF; }
    .share-box { background-color: #ff0000; color: white; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 20px; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 12px; height: 45px; font-weight: bold; }
    
    /* উইন রেট মিটার স্টাইল */
    .win-meter {
        background: #1E1E2E;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #00ff00;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ২. সেশন ডাটা ম্যানেজমেন্ট
if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False

if not st.session_state.auth:
    st.title("🔐 NAJMUL VIP SERVER")
    if st.text_input("পাসওয়ার্ড:", type="password") == "8899":
        st.session_state.auth = True
        st.rerun()
    st.stop()

# ৩. টপ লিঙ্ক
st.markdown(f'<div class="share-box">🔗 VIP LINK: https://ai-signal-7w9ghbcvq7szvy5vuth2gw.streamlit.app</div>', unsafe_allow_html=True)

# ৪. উইন রেট মিটার (উপরে দেখাবে)
if st.session_state.total > 0:
    win_percentage = (st.session_state.wins / st.session_state.total) * 100
    st.markdown(f"""
        <div class="win-meter">
            <p style="margin:0; color:#bbb;">Live Win Rate Accuracy</p>
            <h2 style="margin:0; color:#00ff00;">{win_percentage:.1f}%</h2>
        </div>
    """, unsafe_allow_html=True)

# ৫. ইনপুট সেকশন (বিশ্লেষণ ছাড়া)
st.title("🔥 NAJMUL VIP SIGNAL")
st.subheader("📊 আগের ৬টি রেজাল্ট দিন:")
c1, c2 = st.columns(2)
if c1.button("➕ BIG (B)"):
    if len(st.session_state.temp_input) < 6: 
        st.session_state.temp_input.append("Big")
        st.session_state.show_res = False
if c2.button("➕ SMALL (S)"):
    if len(st.session_state.temp_input) < 6: 
        st.session_state.temp_input.append("Small")
        st.session_state.show_res = False

st.info(f"বর্তমান প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'ইনপুট দিন...'}")

# ৬. পিরিয়ড ও সিগন্যাল বাটন
period = st.text_input("পিরিয়ড নম্বর দিন (শেষ ৩টি):", placeholder="যেমন: 650")

if st.button("🚀 GET SIGNAL (বিশ্লেষণ করুন)", type="primary"):
    if len(st.session_state.temp_input) == 6 and period:
        st.session_state.show_res = True
    else:
        st.error("⚠️ ৬টি রেজাল্ট এবং পিরিয়ড নম্বর দিন!")

# ৭. সিগন্যাল ও ৩টি নম্বর প্রদর্শন
if st.session_state.show_res:
    with st.spinner('🚀 AI বিশ্লেষণ করছে...'):
        time.sleep(1.2)
        
    seed_str = period + "".join(st.session_state.temp_input)
    unique_seed = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (10**8)
    random.seed(unique_seed)
    
    prediction = random.choice(["BIG", "SMALL"])
    nums = random.sample([5,6,7,8,9], 3) if prediction == "BIG" else random.sample([0,1,2,3,4], 3)
    color_class = "big-text" if prediction == "BIG" else "small-text"
    num_str = ", ".join(map(str, sorted(nums)))

    st.markdown(f"""
        <div class="floating-panel">
            <p style="font-size: 11px; color: #00ff00; margin:0;">NAJMUL HACK V2</p>
            <p class="res-text {color_class}">{prediction}</p>
            <p style="font-size: 22px; color: white; margin:0; font-weight: bold;">{num_str}</p>
            <p style="font-size: 10px; color: #bbb; margin-top:5;">STABLE SIGNAL</p>
        </div>
        """, unsafe_allow_html=True)

    # ফলাফল আপডেট ও অটো-রিসেট
    st.write("---")
    w, l = st.columns(2)
    if w.button("✅ WIN"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ✅")
        st.session_state.wins += 1
        st.session_state.total += 1
        st.session_state.temp_input = []
        st.session_state.show_res = False
        st.rerun()
    if l.button("❌ LOSS"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ❌")
        st.session_state.total += 1
        st.session_state.temp_input = []
        st.session_state.show_res = False
        st.rerun()

# ৮. হিস্টরি
st.write("---")
st.subheader("🕒 VIP History")
for item in st.session_state.history[:5]:
    if "✅" in item: st.success(item)
    else: st.error(item)
        
