# pages/shortlist_outreach.py
import streamlit as st
import pandas as pd

# Load your influencer data (similar to load_data())
df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)
df_success = df[df["status"] == "Success"]

st.set_page_config(page_title="Shortlist", layout="wide")

# Navigation button
st.markdown("<div style='text-align:right'><a href='/outreach' target='_self'><button>Go to Outreach Page 🚀</button></a></div>", unsafe_allow_html=True)

st.title("📋 Shortlisted Influencers")

shortlist = st.session_state.get("shortlist", [])

if not shortlist:
    st.warning("No influencers shortlisted yet.")
else:
    if "send_list" not in st.session_state:
        st.session_state.send_list = []

    for username in shortlist:
        row = df_success[df_success["username"] == username].squeeze()

        if row.empty:
            continue

        cols = st.columns([1, 3, 2, 2, 1])
        with cols[0]:
            st.image(row.get("profile_pic_url", "https://via.placeholder.com/60"), width=60)
        with cols[1]:
            st.markdown(f"**@{row['username']}**")
            st.caption(row.get("bio", "No bio"))
        with cols[2]:
            st.markdown(f"**Niche:** {row['Niche']}")
            st.markdown(f"**Instagram:** {int(row['followers']):,} followers")
        with cols[3]:
            yt_subs = row.get("subscribers")
            st.markdown(f"**YouTube:** {int(yt_subs):,} subscribers" if pd.notna(yt_subs) else "No YouTube data")
        with cols[4]:
            if st.checkbox("DM?", key=f"dm_{username}"):
                if username not in st.session_state.send_list:
                    st.session_state.send_list.append(username)
            else:
                if username in st.session_state.send_list:
                    st.session_state.send_list.remove(username)
