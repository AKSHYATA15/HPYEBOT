import streamlit as st

st.set_page_config(page_title="Shortlist", layout="wide")

st.title("📋 Shortlisted Influencers")

if "shortlisted_influencers" not in st.session_state or not st.session_state.shortlisted_influencers:
    st.warning("No influencers have been shortlisted yet.")
    st.stop()

selected_for_outreach = []

for influencer in st.session_state.shortlisted_influencers:
    cols = st.columns(6)
    with cols[0]:
        st.write(f"**{influencer['username']}**")
    with cols[1]:
        st.write(f"**Bio:** {influencer['bio'] or 'No bio'}")
    with cols[2]:
        st.metric("Followers", f"{int(influencer['followers']):,}")
    with cols[3]:
        st.metric("Subscribers", f"{int(influencer['subscribers']):,}" if influencer['subscribers'] else "N/A")
    with cols[4]:
        st.checkbox("Select for Outreach", key=f"select_{influencer['username']}", 
                    value=True, on_change=lambda u=influencer['username']: selected_for_outreach.append(u))
    

# Button to go to outreach page
if st.button("➡️ Go to Outreach Page", use_container_width=True):
    # Store selected influencers
    selected = [inf for inf in st.session_state.shortlisted_influencers 
                if st.session_state.get(f"select_{inf['username']}", False)]

    if not selected:
        st.error("Please select at least one influencer for outreach.")
    else:
        st.session_state.outreach_influencers = selected
        st.switch_page("outreach.py")

