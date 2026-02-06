import streamlit as st
import time
import random

# ১. সেটিংস ও ড্র্যাগেবল (Draggable) ভাসমান উইন্ডো CSS
st.set_page_config(page_title="NAJMUL VIP SIGNAL", layout="centered")

st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #0E1117; color: white; }

    /* ভাসমান প্যানেল ডিজাইন */
    #floating-panel {
        position: fixed;
        top: 100px;
        right: 10px;
        width: 180px;
        background: rgba(20, 22, 30, 0.95);
        border: 2px solid #00ff00;
        border-radius: 20px;
        padding: 15px;
        z-index: 9999;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.4);
        cursor: move; /* মাউস বা আঙুল দিয়ে সরানোর সংকেত */
    }

    .res-text { font-size: 24px; font-weight: bold; margin: 5px 0; }
    .big-text { color: #FF3131; }
    .small-text { color: #00D4FF; }
    </style>

    <script>
    // ড্র্যাগিং লজিক (যাতে স্ক্রিনে যেকোনো জায়গায় সরানো যায়)
    const panel = document.getElementById("floating-panel");
    let isDragging = false;
    panel.onmousedown = (e) => isDragging = true;
    document.onmousemove = (e) => {
        if (isDragging) {
            panel.style.left = e.pageX - 90 + "px";
            panel.style.top = e.pageY - 50 + "px";
        }
    }
    document.onmouseup = () => isDragging = false;
    </script>
    """, unsafe_allow_html=True)

# ২. সেশন ডাটা
if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []
if "temp_input" not in st.session_state: st.session_state.temp_input = []

if not st.session_state.auth:
    st.title("🔐 NAJMUL VIP ACCESS")
    if st.text_input("পাসওয়ার্ড:", type="password") == "8899":
        st.session_state.auth = True
        st.rerun()
    st.stop()

# ৩. মূল ইনপুট সেকশন
st.title("🔥 NAJMUL VIP SIGNAL")
st.subheader("📊 ৬টি রেজাল্ট দিন:")
c1, c2, c3 = st.columns(3)
if c1.button("➕ BIG (B)"):
    if len(st.session_state.temp_input) < 6: st.session_state.temp_input.append("Big")
if c2.button("➕ SMALL (S)"):
    if len(st.session_state.temp_input) < 6: st.session_state.temp_input.append("Small")
if c3.button("🔄 CLEAR"): st.session_state.temp_input = []

st.write(f"প্যাটার্ন: **{' ➡️ '.join(st.session_state.temp_input)}**")
period = st.text_input("পিরিয়ড নম্বর:", placeholder="উদা: 612")

# ৪. সিগন্যাল ক্যালকুলেশন
if period and len(st.session_state.temp_input) == 6:
    random.seed(period)
    prediction = random.choice(["BIG", "SMALL"])
    nums = random.sample([5,6,7,8,9], 2) if prediction == "BIG" else random.sample([0,1,2,3,4], 2)
    num_str = ",".join(map(str, nums))
    
    # ৫. ভাসমান বক্সের সিগন্যাল প্রদর্শন
    color_class = "big-text" if prediction == "BIG" else "small-text"
    st.markdown(f"""
        <div id="floating-panel">
            <p style="font-size: 10px; color: #00ff00; margin:0;">NAJMUL HACK</p>
            <p class="res-text {color_class}">{prediction}</p>
            <p style="font-size: 18px; color: white; margin:0;">{num_str}</p>
            <p style="font-size: 10px; color: #bbb; margin-top:5;">ACTIVE</p>
        </div>
        """, unsafe_allow_html=True)

    # ৬. উইন/লস ও অটো-ক্লিয়ার
    w, l = st.columns(2)
    if w.button("✅ WIN"):
        st.session_state.history.insert(0, f"P {period}: {prediction} ✅")
        st.session_state.temp_input = []
        st.rerun()
    if l.button("❌ LOSS"):
        st.session_state.history.insert(0, f"P {period}: {prediction} ❌")
        st.session_state.temp_input = []
        st.rerun()

# হিস্টরি
st.write("---")
st.subheader("🕒 History")
for item in st.session_state.history[:3]:
    st.write(item)
    
