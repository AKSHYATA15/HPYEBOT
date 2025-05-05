import streamlit as st
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired
import time

st.set_page_config(page_title="Outreach", layout="wide")
st.title("📨 Outreach Automation")

st.markdown("""
    <style>
    .main {
    background-color: #f8f9fa;
}
[data-testid="stSidebar"] {
    padding: 2.5rem 1.5rem !important;
    box-shadow: 5px 0 15px rgba(0,0,0,0.1);
}
[data-testid="stSidebarNav"] > ul {
    font-size: 1.15rem;
    gap: 12px;
}
[data-testid="stSidebarNav"] ul li {
    margin-bottom: 20px;
    font-weight: 500;
    transition: all 0.3s ease;
    padding: 8px 12px;
    border-radius: 6px;
}
[data-testid="stSidebarNav"] ul li:hover {
    background: rgba(0,0,0,0.05);
    transform: translateX(5px);
}
    
    </style>
""", unsafe_allow_html=True)

# Check if there are selected influencers
if "outreach_influencers" not in st.session_state or not st.session_state.outreach_influencers:
    st.warning("No influencers selected for outreach.")
    st.stop()

# Login form for Instagram
with st.form("login_form"):
    st.subheader("Login to Instagram")
    username = st.text_input("Instagram Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    cl = Client()

    with st.spinner("Logging in... Please wait. If this takes too long, try logging into your account manually from your device to authenticate this login activity."):
        try:
            cl.login(username, password)
            st.session_state.client = cl
            st.success("Login successful!")
        except ChallengeRequired:
            st.error("Instagram requires verification. Please login from your device first.")
        except LoginRequired:
            st.error("Login required. Please check your credentials.")
        except Exception as e:
            st.error(f"Login failed: {str(e)}")

# Once logged in, allow sending DMs
if "client" in st.session_state:
    cl = st.session_state.client

    st.subheader("Send DMs to Selected Influencers")

    dm_message = st.text_area("Enter your DM message")

    if st.button("Send DMs 🚀"):
        for influencer in st.session_state.outreach_influencers:
            username = influencer["username"]
            try:
                user_id = cl.user_id_from_username(username)
                cl.direct_send(dm_message, [user_id])
                st.success(f"DM sent to @{username}")
                time.sleep(2)  # Delay to avoid spam
            except Exception as e:
                st.error(f"Failed to send DM to @{username}: {str(e)}")

