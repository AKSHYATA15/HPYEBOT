import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shortlist", layout="wide")

st.title("📋 Shortlisted Influencers")

# Top-right navigation button
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
    .top-right-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown('<div class="top-right-button"><a href="/outreach" target="_self"><button>➡️ Go to Outreach Page</button></a></div>', unsafe_allow_html=True)

if "shortlisted_influencers" not in st.session_state or not st.session_state.shortlisted_influencers:
    st.warning("No influencers have been shortlisted yet.")
    st.stop()

# Display influencers
for influencer in st.session_state.shortlisted_influencers:
    cols = st.columns(6)
    with cols[0]:
        st.write(f"**{influencer['username']}**")
    with cols[1]:
        st.metric("Followers", f"{int(influencer['followers']):,}" if pd.notna(influencer['followers']) else "N/A")
    with cols[2]:
        st.metric("Subscribers", f"{int(influencer['subscribers']):,}" if pd.notna(influencer['subscribers']) else "N/A")
    with cols[3]:
        st.write(influencer.get("bio", ""))
    with cols[4]:
        st.write(f"Niche: {influencer.get('Niche', 'N/A')}")
    with cols[5]:
        st.checkbox("Select for Outreach", key=f"select_{influencer['username']}", value=True)

st.markdown("---")

# Final button
if st.button("✅ Confirm and Go to Outreach Page"):
    selected = [
        inf for inf in st.session_state.shortlisted_influencers
        if st.session_state.get(f"select_{inf['username']}", False)
    ]

    if not selected:
        st.error("Please select at least one influencer for outreach.")
    else:
        st.session_state.outreach_influencers = selected
        st.success("Influencers selected. Redirecting...")
        st.switch_page("pages/📤Outreach.py")
