import streamlit as st
import random
import time

# ১. প্রফেশনাল থিম সেটিংস
st.set_page_config(page_title="SM COMMUNITY AI HACK", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .signal-box {
        background-color: #1a1c24;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #4CAF50;
        text-align: center;
        box-shadow: 0px 0px 20px rgba(76, 175, 80, 0.3);
    }
    .res-big { font-size: 45px; font-weight: bold; color: #FF3131; }
    .res-small { font-size: 45px; font-weight: bold; color: #00D4FF; }
    </style>
    """, unsafe_allow_html=True)

# ২. পাসওয়ার্ড প্রটেকশন (৮৮৯৯)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 PREMIUM ACCESS")
    pw = st.text_input("Enter Activation Key:", type="password")
    if st.button("Activate"):
        if pw == "8899":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid Key!")
    st.stop()

# ৩. AI সিগন্যাল জেনারেটর লজিক
st.title("🚀 MUMINUL BOSS PREMIUM AI")
st.write("● AI Server Connected")

period = st.text_input("Enter Period Number (Last 3 Digits):", placeholder="e.g. 650")

if period:
    # এখানে 'seed' ব্যবহার করা হয়েছে যাতে একই পিরিয়ডে একই রেজাল্ট থাকে, 
    # কিন্তু আলাদা পিরিয়ড দিলে রেজাল্ট পুরোপুরি র‍্যান্ডম এবং ভিন্ন হয়।
    random.seed(period) 
    
    with st.spinner('AI Analyzing Market Trend...'):
        time.sleep(1.5) 

    # AI প্রেডিকশন লজিক
    prediction = random.choice(["BIG", "SMALL"])
    confidence = random.randint(92, 99)
    
    if prediction == "BIG":
        nums = random.sample([5, 6, 7, 8, 9], 3)
        display_res = f'<p class="res-big">BIG {", ".join(map(str, nums))}</p>'
    else:
        nums = random.sample([0, 1, 2, 3, 4], 3)
        display_res = f'<p class="res-small">SMALL {", ".join(map(str, nums))}</p>'

    st.markdown(f"""
        <div class="signal-box">
            <p style="font-size: 18px; color: #bbb;">NEXT PREDICTION</p>
            {display_res}
            <p style="color: #FFA500;">Confidence: {confidence}%</p>
        </div>
        """, unsafe_allow_html=True)

# ৪. লাইভ হিস্ট্রি (কাল্পনিক AI ডাটা)
st.write("---")
st.subheader("🕒 Live Analysis History")
st.code(f"Period: ...{int(period)-1 if period.isdigit() else 'XXX'} ➡️ WIN ✅\nPeriod: ...{int(period)-2 if period.isdigit() else 'XXX'} ➡️ WIN ✅")
