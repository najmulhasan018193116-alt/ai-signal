import streamlit as st
import time
import random
import hashlib

# ১. প্রিমিয়াম ডিজাইন ও সেটিংস
st.set_page_config(page_title="NAJMUL VIP PRO", layout="centered")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #05070A; color: white; }
    
    .floating-panel {
        position: fixed;
        top: 80px;
        right: 10px;
        width: 180px;
        background: rgba(10, 15, 30, 0.95);
        border: 2px solid #00FFCC;
        border-radius: 20px;
        padding: 15px;
        z-index: 9999;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.4);
    }
    .res-text { font-size: 32px; font-weight: 900; margin: 5px 0; }
    .big-text { color: #FF4B4B; text-shadow: 0 0 15px #FF4B4B; }
    .small-text { color: #00D4FF; text-shadow: 0 0 15px #00D4FF; }
    .share-box { background: linear-gradient(90deg, #FF0000, #990000); color: white; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 20px; font-weight: bold; border: 1px solid white; }
    .stButton>button { width: 100%; border-radius: 15px; height: 50px; font-weight: bold; font-size: 16px; }
    .get-btn>div>button { background: #FF3131 !important; color: white !important; border: 2px solid white !important; font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

# ২. সেশন ডাটা ম্যানেজমেন্ট
if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []
if "wins" not in st.session_state: st.session_state.wins = 0
if "total" not in st.session_state: st.session_state.total = 0
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "show_res" not in st.session_state: st.session_state.show_res = False

# ৩. পাসওয়ার্ড প্রটেকশন (পুনরায় যোগ করা হয়েছে)
if not st.session_state.auth:
    st.title("🔐 NAJMUL VIP SERVER")
    pw = st.text_input("পাসওয়ার্ড প্রবেশ করান:", type="password")
    if st.button("LOGIN"):
        if pw == "8899":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ ভুল পাসওয়ার্ড!")
    st.stop()

# ৪. ভিআইপি লিঙ্ক এবং একুরেসি মিটার
st.markdown(f'<div class="share-box">🔗 VIP SERVER ACTIVE: https://ai-signal-7w9ghbcvq7szvy5vuth2gw.streamlit.app</div>', unsafe_allow_html=True)

if st.session_state.total > 0:
    acc = (st.session_state.wins / st.session_state.total) * 100
    st.metric("Live Accuracy", f"{acc:.1f}%")

# ৫. মেইন ইনপুট সেকশন
st.title("🚀 NAJMUL VIP PRO V3")
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

st.info(f"প্যাটার্ন: {' ➡️ '.join(st.session_state.temp_input) if st.session_state.temp_input else 'ইনপুট দিন...'}")

# ৬. পিরিয়ড ও সিগন্যাল ট্রিগার
period = st.text_input("পিরিয়ড নম্বর দিন (শেষ ৩টি):", placeholder="উদা: 644")

st.markdown('<div class="get-btn">', unsafe_allow_html=True)
if st.button("🚀 GET SIGNAL (বিশ্লেষণ করুন)"):
    if len(st.session_state.temp_input) == 6 and period:
        st.session_state.show_res = True
    else:
        st.warning("⚠️ ৬টি রেজাল্ট এবং পিরিয়ড নম্বর দিন!")

# ৭. প্রো-লেভেল অ্যালগরিদম ও ৩টি নম্বর
if st.session_state.show_res:
    with st.spinner('🔍 AI বিশ্লেষণ করছে...'):
        time.sleep(1.5)
    
    seed_str = period + "".join(st.session_state.temp_input)
    unique_seed = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16)
    random.seed(unique_seed)
    
    prediction = random.choice(["BIG", "SMALL"])
    nums = random.sample([5,6,7,8,9], 3) if prediction == "BIG" else random.sample([0,1,2,3,4], 3)
    color_class = "big-text" if prediction == "BIG" else "small-text"
    num_str = ", ".join(map(str, sorted(nums)))

    st.markdown(f"""
        <div class="floating-panel">
            <p style="font-size: 11px; color: #00FFCC; margin:0; font-weight:bold;">NAJMUL HACK V3</p>
            <p class="res-text {color_class}">{prediction}</p>
            <p style="font-size: 24px; color: white; margin:0; font-weight: 900;">{num_str}</p>
            <p style="font-size: 10px; color: #999; margin-top:5;">STABLE AI SIGNAL</p>
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

# ৯. হিস্টরি সেকশন
st.write("---")
st.subheader("🕒 VIP History")
for item in st.session_state.history[:5]:
    if "✅" in item: st.success(item)
    else: st.error(item)
    
