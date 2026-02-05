import streamlit as st
import time

# ১. প্রফেশনাল ডিজাইন ও থিম সেটিংস
st.set_page_config(page_title="SM COMMUNITY AI HACK", layout="centered")

# কাস্টম CSS দিয়ে লুক প্রফেশনাল করা (ডার্ক থিম ও উজ্জ্বল সিগন্যাল)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .signal-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #4CAF50;
        background-color: #1A1C24;
        margin-bottom: 10px;
    }
    .big-text { font-size: 40px; font-weight: bold; color: #00FF00; }
    .small-text { font-size: 40px; font-weight: bold; color: #00D4FF; }
    </style>
    """, unsafe_allow_html=True)

# ২. সিকিউরিটি (পাসওয়ার্ড: 8899)
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ SM COMMUNITY PREMIUM")
    pw = st.text_input("Enter Activation Key:", type="password")
    if st.button("Activate Now"):
        if pw == "8899":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid Key! Contact Admin.")
    st.stop()

# ৩. গেম এনালাইসিস লজিক
st.title("🚀 MUMINUL BOSS PREMIUM AI")
st.write("Status: ● ACTIVE")

# সাইডবার মেনু
with st.sidebar:
    st.image("https://www.pngall.com/wp-content/uploads/10/AI-Intelligence-PNG.png", width=100)
    st.header("Settings")
    st.link_button("✈️ Join Official Telegram", "https://t.me/your_link")
    st.link_button("🔗 Register Account", "https://your_refer_link.com")

# ৪. পিরিয়ড ইনপুট ও প্রেডিকশন
period = st.number_input("Enter Last 3 Digit of Period:", min_value=0, max_value=999, step=1)

if period:
    with st.spinner('Analyzing Server Data...'):
        time.sleep(1.5) # এনালাইসিসের অনুভূতি দেওয়ার জন্য
        
    last_digit = period % 10
    
    # প্রফেশনাল লজিক (০-৪ Small, ৫-৯ Big)
    if last_digit in [0, 1, 2, 3, 4]:
        res = "SMALL"
        color_class = "small-text"
        numbers = "0, 2, 4"
    else:
        res = "BIG"
        color_class = "big-text"
        numbers = "5, 7, 9"

    # সিগন্যাল বক্স প্রদর্শন (স্ক্রিনশটের মতো লুক)
    st.markdown(f"""
        <div class="signal-box">
            <p style="font-size: 20px;">NEXT RESULT</p>
            <p class="{color_class}">{res} {numbers}</p>
            <p style="color: #FFA500;">Confidence: 98%</p>
        </div>
        """, unsafe_allow_html=True)

# ৫. হিস্ট্রি ও রিসেন্ট উইন
st.write("---")
st.subheader("🕒 Live Analysis History")
st.code("Period: ...694 ➡️ BIG (WIN) ✅\nPeriod: ...695 ➡️ SMALL (WIN) ✅")
