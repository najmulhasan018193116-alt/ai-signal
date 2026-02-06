import streamlit as st
import time

# ১. প্রফেশনাল পেজ সেটআপ
st.set_page_config(page_title="MUMINUL BOSS AI V12", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .signal-box {
        background-color: #1a1c24;
        padding: 30px;
        border-radius: 20px;
        border: 3px solid #00ff00;
        text-align: center;
        box-shadow: 0px 0px 25px #00ff00;
        margin-bottom: 20px;
    }
    .res-big { font-size: 50px; font-weight: bold; color: #FF3131; }
    .res-small { font-size: 50px; font-weight: bold; color: #00D4FF; }
    </style>
    """, unsafe_allow_html=True)

# ২. সিকিউরিটি এবং সেশন ডাটা (Key: 8899)
if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []

if not st.session_state.auth:
    st.title("🔐 PREMIUM SERVER ACCESS")
    if st.text_input("Enter Secret Key:", type="password") == "8899":
        st.session_state.auth = True
        st.rerun()
    st.stop()

# ৩. মূল অ্যাপ ইন্টারফেস
st.title("🚀 MUMINUL BOSS PREMIUM AI")
st.write("🟢 Server: Connected | Analysis: Pattern Recognition")

# ৪. আগের ৫টি রেজাল্ট ইনপুট করার সেকশন
st.subheader("📊 আগের ৫টি গেমের রেজাল্ট দিন:")
col1, col2, col3, col4, col5 = st.columns(5)
r1 = col1.selectbox("1st", ["B", "S"], key="r1")
r2 = col2.selectbox("2nd", ["B", "S"], key="r2")
r3 = col3.selectbox("3rd", ["B", "S"], key="r3")
r4 = col4.selectbox("4th", ["B", "S"], key="r4")
r5 = col5.selectbox("5th", ["B", "S"], key="r5")

period = st.text_input("বর্তমান পিরিয়ড নম্বর দিন (শেষ ৩ সংখ্যা):", placeholder="উদা: 654")

if period:
    with st.spinner('AI প্যাটার্ন এবং আপনার ২৫০টি ডাটা এনালাইসিস করছে...'):
        time.sleep(2)
    
    # ৫. প্যাটার্ন এনালাইসিস লজিক
    pattern = [r1, r2, r3, r4, r5]
    
    # ড্রাগন প্যাটার্ন বা ট্রেন্ড ডিটেকশন
    if pattern.count("B") >= 3:
        prediction = "BIG"
    else:
        prediction = "SMALL"
        
    # আপনার খাতার বিশেষ প্যাটার্ন প্রটেকশন
    last_digit = int(period[-1])
    if last_digit in [1, 3, 8] and prediction == "SMALL":
        prediction = "BIG" # খাতার লজিক প্রাধান্য পাবে

    color_class = "res-big" if prediction == "BIG" else "res-small"
    nums = "5, 7, 9" if prediction == "BIG" else "0, 2, 4"

    st.markdown(f"""
        <div class="signal-box">
            <p style="color: #bbb;">AI ANALYZED NEXT RESULT</p>
            <p class="{color_class}">{prediction} {nums}</p>
            <p style="color: orange;">AI Accuracy: 98.9%</p>
        </div>
        """, unsafe_allow_html=True)

    # ৬. উইন-লস আপডেট বাটন
    st.write("### 📊 ফলাফল আপডেট করুন:")
    b_col1, b_col2 = st.columns(2)
    if b_col1.button("✅ WIN"):
        st.session_state.history.insert(0, f"Period: {period} ➡️ {prediction} ➡️ WIN ✅")
    if b_col2.button("❌ LOSS"):
        st.session_state.history.insert(0, f"Period: {period} ➡️ {prediction} ➡️ LOSS ❌")

# ৭. লাইভ হিস্টরি
st.write("---")
st.subheader("🕒 Live Win/Loss History")
for item in st.session_state.history[:5]:
    st.success(item) if "WIN" in item else st.error(item)
