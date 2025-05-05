import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shortlist", layout="wide")

if "shortlisted" not in st.session_state:
    st.session_state["shortlisted"] = []

if "outreach_list" not in st.session_state:
    st.session_state["outreach_list"] = []

st.title("📋 Shortlisted Influencers")
st.markdown("<div style='text-align: right'><a href='/outreach' target='_self'><button>Go to Outreach Page</button></a></div>", unsafe_allow_html=True)

selected_for_outreach = []

if not st.session_state["shortlisted"]:
    st.info("No influencers shortlisted.")
else:
    for idx, influencer in enumerate(st.session_state["shortlisted"]):
        with st.container():
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(influencer.get("profile_pic_url", "https://via.placeholder.com/60"), width=60)
            with col2:
                st.write(f"**@{influencer['username']}**")
                st.write(f"Bio: {influencer.get('bio', 'No bio')}")
                st.write(f"Niche: {influencer['Niche']}, Followers: {influencer['followers']}, Subscribers: {influencer.get('subscribers', 'N/A')}")
                if st.checkbox("Select for Outreach", key=f"outreach_{influencer['username']}"):
                    selected_for_outreach.append(influencer)
