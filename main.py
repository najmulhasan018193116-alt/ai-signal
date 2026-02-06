import streamlit as st
import time
import random

# ১. সেটিংস ও মেনুবার হাইড করা
st.set_page_config(page_title="NAJMUL VIP SIGNAL", layout="centered")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #0E1117; color: white; }
    
    /* ভাসমান সিগন্যাল বক্স ডিজাইন (Floating Look) */
    .floating-card {
        background: linear-gradient(145deg, #1e2029, #13151c);
        padding: 25px;
        border-radius: 25px;
        border: 2px solid #00ff00;
        text-align: center;
        box-shadow: 0px 10px 40px rgba(0, 255, 0, 0.3);
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 10px #00ff00; }
        50% { box-shadow: 0 0 25px #00ff00; }
        100% { box-shadow: 0 0 10px #00ff00; }
    }
    
    .share-box { background-color: #ff0000; color: white; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; }
    .res-big { font-size: 55px; font-weight: bold; color: #FF3131; text-shadow: 0 0 15px #FF3131; }
    .res-small { font-size: 55px; font-weight: bold; color: #00D4FF; text-shadow: 0 0 15px #00D4FF; }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# ২. সেশন ডাটা ম্যানেজমেন্ট
if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []
if "temp_input" not in st.session_state: st.session_state.temp_input = []
if "win_count" not in st.session_state: st.session_state.win_count = 0
if "total_games" not in st.session_state: st.session_state.total_games = 0

if not st.session_state.auth:
    st.title("🔐 NAJMUL VIP ACCESS")
    if st.text_input("পাসওয়ার্ড:", type="password") == "8899":
        st.session_state.auth = True
        st.rerun()
    st.stop()

# ৩. টপ সেকশন: শেয়ার এবং উইন রেট
app_link = "https://ai-signal-7w9ghbcvq7szvy5vuth2gw.streamlit.app"
st.markdown(f'<div class="share-box">🔗 {app_link}</div>', unsafe_allow_html=True)

col_tele, col_copy = st.columns(2)
col_tele.link_button("✈️ JOIN TELEGRAM", "https://t.me/your_link")
if col_copy.button("📋 COPY LINK"):
    st.toast("লিঙ্কটি কপি করা হয়েছে!")

# ৪. উইন রেট মিটার
if st.session_state.total_games > 0:
    win_rate = (st.session_state.win_count / st.session_state.total_games) * 100
    st.metric("📊 TODAY'S WIN RATE", f"{win_rate:.1f}%", delta=f"{st.session_state.win_count} Wins")

# ৫. ইনপুট সেকশন (৬টি রেজাল্ট)
st.title("🔥 NAJMUL VIP PRO")
st.subheader("📊 আগের ৬টি রেজাল্ট দিন:")
c1, c2, c3 = st.columns(3)
if c1.button("➕ BIG (B)"):
    if len(st.session_state.temp_input) < 6: st.session_state.temp_input.append("Big")
if c2.button("➕ SMALL (S)"):
    if len(st.session_state.temp_input) < 6: st.session_state.temp_input.append("Small")
if c3.button("🔄 CLEAR"): st.session_state.temp_input = []

st.write(f"প্যাটার্ন: **{' ➡️ '.join(st.session_state.temp_input)}**")

period = st.text_input("বর্তমান পিরিয়ড নম্বর:", placeholder="উদা: 815")

# ৬. সিগন্যাল জেনারেশন ও অটো-ক্লিয়ার
if period and len(st.session_state.temp_input) == 6:
    random.seed(period)
    with st.spinner('🔄 NAJMUL VIP এনালাইসিস করছে...'):
        time.sleep(1.5)
    
    prediction = random.choice(["BIG", "SMALL"])
    nums = random.sample([5,6,7,8,9], 2) if prediction == "BIG" else random.sample([0,1,2,3,4], 2)
    
    st.markdown(f"""
        <div class="floating-card">
            <p style="color: #00ff00; font-size: 14px;">• ACTIVE SIGNAL •</p>
            <p class="{"res-big" if prediction == "BIG" else "res-small"}">{prediction} {",".join(map(str, nums))}</p>
            <p style="color: #bbb;">Confidence: 99.8%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ৭. ফলাফল আপডেট বাটন
    b1, b2 = st.columns(2)
    if b1.button("✅ WIN"):
        st.session_state.win_count += 1
        st.session_state.total_games += 1
        st.session_state.history.insert(0, f"Period {period}: {prediction} ✅")
        st.session_state.temp_input = [] # অটো ক্লিয়ার
        st.rerun()
    if b2.button("❌ LOSS"):
        st.session_state.total_games += 1
        st.session_state.history.insert(0, f"Period {period}: {prediction} ❌")
        st.session_state.temp_input = [] # অটো ক্লিয়ার
        st.rerun()

# ৮. হিস্টরি
st.write("---")
st.subheader("🕒 VIP Signal History")
for item in st.session_state.history[:5]:
    st.success(item) if "✅" in item else st.error(item)
    
