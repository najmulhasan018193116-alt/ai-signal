import streamlit as st
import collections

# --- ১. পাসওয়ার্ড ও নিরাপত্তা সেটিংস ---
# পাসওয়ার্ড পরিবর্তন করতে চাইলে নিচের "123" এর জায়গায় আপনার নতুন পাসওয়ার্ড লিখুন
SECURITY_PASSWORD = "123" 

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if not st.session_state.authenticated:
        st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🔒 AI System Secure Login</h2>", unsafe_allow_html=True)
        pwd = st.text_input("সিকিউরিটি পাসওয়ার্ড দিন:", type="password")
        if st.button("প্রবেশ করুন"):
            if pwd == SECURITY_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
        return False
    return True

# পাসওয়ার্ড সঠিক হলে নিচের অংশটি কাজ করবে
if check_password():
    # --- ২. অ্যাপের মূল কনফিগারেশন ---
    st.set_page_config(page_title="Advanced AI Predictor", layout="centered")
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎯 FULL AI SIGNAL SYSTEM PRO</h1>", unsafe_allow_html=True)

    # সেশন মেমোরি সেটআপ (যাতে অ্যাপ রিফ্রেশ হলেও ডেটা না হারায়)
    if 'history' not in st.session_state:
        st.session_state.history = [] 
    if 'bet_amount' not in st.session_state:
        st.session_state.bet_amount = 10
    if 'base_bet' not in st.session_state:
        st.session_state.base_bet = 10

    # --- ৩. রিসেট প্যানেল (সাইডবারে) ---
    st.sidebar.header("🛠️ সিস্টেম কন্ট্রোল")
    
    # পুরোনো হিস্ট্রি রিসেট করার বাটন
    if st.sidebar.button("🗑️ পুরোনো হিস্ট্রি রিসেট করুন"):
        st.session_state.history = []
        st.session_state.bet_amount = st.session_state.base_bet
        st.sidebar.success("সব পুরোনো ডেটা মুছে ফেলা হয়েছে!")
        st.rerun()

    # ইনভেস্টমেন্ট রিসেট করার বাটন
    if st.sidebar.button("💰 শুধু ইনভেস্টমেন্ট রিসেট"):
        st.session_state.bet_amount = st.session_state.base_bet
        st.rerun()

    # --- ৪. AI প্রেডিকশন ইঞ্জিন ---
    def predict_engine(data):
        if len(data) < 4: return None, 0
        current_pattern = tuple(data[-3:])
        matches = [data[i+3] for i in range(len(data)-3) if tuple(data[i:i+3]) == current_pattern]
        
        if not matches:
            # যদি কোনো মিল না পায় তবে বিপরীত ট্রেন্ড ফলো করবে
            prediction = 'B' if data[-1] == 'S' else 'S'
            return prediction, 50
        
        prediction = collections.Counter(matches).most_common(1)[0][0]
        confidence = (matches.count(prediction) / len(matches)) * 100
        return prediction, confidence

    # --- ৫. সিগন্যাল ডিসপ্লে ---
    next_p, conf = predict_engine(st.session_state.history)

    if next_p:
        color = "#4CAF50" if next_p == 'B' else "#2196F3"
        st.markdown(f"""
        <div style="background-color:{color}; padding:25px; border-radius:15px; text-align:center; border: 3px solid white; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
            <h2 style="color:white; margin:0; font-family:Arial;">পরবর্তী সিগন্যাল: {'BIG' if next_p == 'B' else 'SMALL'}</h2>
            <h3 style="color:white; margin:10px 0;">সম্ভাবনা: {conf:.1f}%</h3>
            <h2 style="color:#FFD700; margin:0;">💰 ইনভেস্ট: {st.session_state.bet_amount} টাকা</h2>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ সিস্টেম অ্যানালাইজ করতে আরও {4 - len(st.session_state.history)} টি রেজাল্ট দিন।")

    st.write("---")

    # --- ৬. উইন/লস বাটন (অটো-ক্যালকুলেশন) ---
    st.write("### 💵 ফলাফল আপডেট (Martingale)")
    col_win, col_loss = st.columns(2)
    
    with col_win:
        if st.button("✅ WIN", use_container_width=True):
            if next_p:
                st.session_state.history.append(next_p)
                st.session_state.bet_amount = st.session_state.base_bet # জিতলে ১০ টাকায় ফেরত
                st.balloons() # সেলিব্রেশন ইফেক্ট
                st.rerun()

    with col_loss:
        if st.button("❌ LOSS", use_container_width=True):
            if next_p:
                actual = 'S' if next_p == 'B' else 'B'
                st.session_state.history.append(actual)
                st.session_state.bet_amount *= 3 # হারলে ৩ গুণ ইনভেস্ট
                st.rerun()

    st.write("---")

    # --- ৭. নতুন রেজাল্ট যোগ করার বাটন ---
    st.write("### 🆕 গেম রেজাল্ট আপডেট করুন")
    col_b, col_s = st.columns(2)
    with col_b:
        if st.button("➕ ADD BIG (B)", use_container_width=True):
            st.session_state.history.append('B')
            st.rerun()
    with col_s:
        if st.button("➕ ADD SMALL (S)", use_container_width=True):
            st.session_state.history.append('S')
            st.rerun()

    # সাম্প্রতিক হিস্ট্রি
    st.write("---")
    st.write(f"**বর্তমান রান টাইম হিস্ট্রি:** {', '.join(st.session_state.history[-15:])}")


        
