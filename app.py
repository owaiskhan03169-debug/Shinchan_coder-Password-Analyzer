import streamlit as st
import math
import re

# Page Configuration
st.set_page_config(page_title="PassGuard - Password Analyzer", page_icon="🔐")

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput>div>div>input {
        background-color: #262730;
        color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC FUNCTIONS ---
def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^a-zA-Z0-9]", password): charset += 32
    
    if charset == 0 or len(password) == 0:
        return 0
    return round(len(password) * math.log2(charset), 2)

def get_crack_time(entropy):
    guesses_per_sec = 1e9
    seconds = (2 ** entropy) / guesses_per_sec
    if seconds < 1: return "Instant"
    if seconds < 3600: return f"{int(seconds/60)} minutes"
    if seconds < 86400: return f"{int(seconds/3600)} hours"
    if seconds < 31536000: return f"{int(seconds/86400)} days"
    return f"{int(seconds/31536000):,} years"

# --- UI LAYOUT ---
st.title("🔐 PassGuard: Password Strength Analyzer")
st.write("Enter a password below to check its mathematical strength (Entropy).")

password = st.text_input("Enter Password", type="password", placeholder="e.g. MySecurePwd!2025")

if password:
    entropy = calculate_entropy(password)
    crack_time = get_crack_time(entropy)
    
    # Metrics Display
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Entropy Bits", f"{entropy} bits")
    with col2:
        st.metric("Time to Crack", crack_time)

    # Strength Progress Bar
    strength = min(entropy / 100, 1.0) # Normalizing for progress bar
    if entropy < 40:
        st.error(f"Strength: WEAK 🔴")
        st.progress(strength)
    elif entropy < 70:
        st.warning(f"Strength: MEDIUM 🟡")
        st.progress(strength)
    else:
        st.success(f"Strength: STRONG 🟢")
        st.progress(strength)

    # Patterns & Tips
    st.subheader("Security Insights")
    if len(password) < 12:
        st.info("💡 Tip: Try making it 12+ characters long.")
    if not re.search(r"[^a-zA-Z0-9]", password):
        st.info("💡 Tip: Add special characters (!@#$) to boost entropy.")

st.divider()
st.caption("Built with Python & Streamlit for Cybersecurity Awareness.")
