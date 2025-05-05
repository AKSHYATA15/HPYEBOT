import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Shortlist Influencers", layout="wide", initial_sidebar_state="collapsed")

# Title and instructions
st.title("📋 Shortlisted Influencers")

# Check if any influencers are selected
if "shortlisted_influencers" not in st.session_state or not st.session_state.shortlisted_influencers:
    st.warning("No influencers selected yet. Please go back to the list page and shortlist influencers.")
    st.stop()

# Load influencer data
df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)

# Filter influencers selected for shortlist
shortlisted_df = df[df['username'].isin(st.session_state.shortlisted_influencers)]

# Display shortlisted influencers
for _, row in shortlisted_df.iterrows():
    cols = st.columns(6)
    
    with cols[0]:
        image_url = row.get("youtube_profile_image", row.get("profile_pic_url"))
        profile_url = f"https://instagram.com/{row['username']}"
        
        if pd.notna(image_url):
            st.markdown(f"[![profile]({image_url})]({profile_url})", unsafe_allow_html=True)
        else:
            st.markdown(f"[![profile](https://via.placeholder.com/60)]({profile_url})", unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"**{row['username']}**")
    
    with cols[2]:
        st.metric("Instagram Followers", f"{int(row['followers']):,}" if pd.notna(row['followers']) else "N/A")
    
    with cols[3]:
        st.metric("YouTube Subscribers", f"{int(row['subscribers']):,}" if pd.notna(row['subscribers']) else "N/A")
    
    with cols[4]:
        st.write(f"**Niche:** {row['Niche']}")
    
    with cols[5]:
        st.write(f"**Bio:** {row['bio'] if pd.notna(row['bio']) else 'No bio available'}")

# Button to proceed to outreach page
if st.button("Go to Outreach Page"):
    # Save the selected influencers to session state to use in outreach.py
    st.session_state.outreach_influencers = st.session_state.shortlisted_influencers
    st.success("You are now ready to send DMs to the selected influencers.")
    st.experimental_rerun()
