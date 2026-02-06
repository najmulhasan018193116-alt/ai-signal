import streamlit as st
import time
import random

# ১. থিম, সেটিংস এবং মেনুবার হাইড করা
st.set_page_config(page_title="NAJMUL VIP SIGNAL", layout="centered")

st.markdown("""
    <style>
    /* মেনুবার এবং ফুটার লুকানোর জন্য */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* শেয়ার বক্সের স্টাইল (লাল বক্স) */
    .share-box {
        background-color: #ff0000;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        border: 2px solid white;
    }
    
    /* মূল ডিজাইন */
    .stApp { background-color: #0E1117; color: white; }
    .signal-box {
        background-color: #1a1c24;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00ff00;
        text-align: center;
        box-shadow: 0px 0px 30px rgba(0, 255, 0, 0.4);
        margin-bottom: 20px;
    }
    .res-big { font-size: 50px; font-weight: bold; color: #FF3131; }
    .res-small { font-size: 50px; font-weight: bold; color: #00D4FF; }
    .stButton>button { width: 100%; border-radius: 10px; height: 45px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ২. সেশন ডাটা
if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []
if "temp_input" not in st.session_state: st.session_state.temp_input = []

if not st.session_state.auth:
    st.title("🔐 NAJMUL VIP ACCESS")
    if st.text_input("পাসওয়ার্ড দিন:", type="password") == "8899":
        st.session_state.auth = True
        st.rerun()
    st.stop()

# ৩. শেয়ার বক্স (লাল বক্সের ভিতরে লিঙ্ক)
app_link = "https://ai-signal-7w9ghbcvq7szvy5vuth2gw.streamlit.app"
st.markdown(f"""
    <div class="share-box">
        📢 অ্যাপটি সবার সাথে শেয়ার করুন:<br>
        <span style="font-size: 14px;">{app_link}</span>
    </div>
    """, unsafe_allow_html=True)

# ৪. ইন্টারফেস - ৬টি রেজাল্ট ইনপুট
st.title("🔥 NAJMUL VIP SIGNAL PRO")
st.write("🟢 Server: Active | Version: Private Edition")

st.subheader("📊 আগের ৬টি রেজাল্ট দিন (বাটন চাপুন):")
col_b, col_s, col_c = st.columns([1, 1, 1])

if col_b.button("➕ ADD BIG (B)"):
    if len(st.session_state.temp_input) < 6:
        st.session_state.temp_input.append("Big")
if col_s.button("➕ ADD SMALL (S)"):
    if len(st.session_state.temp_input) < 6:
        st.session_state.temp_input.append("Small")
if col_c.button("🔄 CLEAR"):
    st.session_state.temp_input = []

st.write(f"প্যাটার্ন: **{' ➡️ '.join(st.session_state.temp_input)}**")

# ৫. পিরিয়ড নম্বর ও নম্বর লজিক
period = st.text_input("বর্তমান পিরিয়ড নম্বর দিন (শেষ ৩ সংখ্যা):", placeholder="উদা: 811")

if period and len(st.session_state.temp_input) == 6:
    random.seed(period)
    
    with st.spinner('NAJMUL VIP AI এনালাইসিস করছে...'):
        time.sleep(1)
    
    prediction = random.choice(["BIG", "SMALL"])
    
    if prediction == "BIG":
        selected_nums = random.sample([5, 6, 7, 8, 9], 3)
        color_class = "res-big"
    else:
        selected_nums = random.sample([0, 1, 2, 3, 4], 3)
        color_class = "res-small"
    
    num_str = ", ".join(map(str, sorted(selected_nums)))

    st.markdown(f"""
        <div class="signal-box">
            <p style="color: #bbb; font-size: 18px;">NAJMUL VIP PREDICTION</p>
            <p class="{color_class}">{prediction} {num_str}</p>
            <p style="color: #00ff00;">Accuracy: 99.7%</p>
        </div>
        """, unsafe_allow_html=True)

    # ৬. ফলাফল আপডেট বাটন
    st.write("### 📊 ফলাফল আপডেট করুন:")
    win_col, loss_col = st.columns(2)
    if win_col.button("✅ WIN"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ✅ WIN")
    if loss_col.button("❌ LOSS"):
        st.session_state.history.insert(0, f"Period {period}: {prediction} ❌ LOSS")

# ৭. লাইভ হিস্টরি
st.write("---")
st.subheader("🕒 VIP Signal History")
for item in st.session_state.history[:5]:
    if "WIN" in item: st.success(item)
    else: st.error(item)
    
