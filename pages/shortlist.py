import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Shortlisted Influencers", layout="wide", initial_sidebar_state="collapsed")

# Header Styling
st.markdown("""
<style>
    .header {
        color: #2e35a0;
        border-bottom: 2px solid #f6a4b9;
        padding-bottom: 10px;
    }
    .metric-box {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #2e35a0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .highlight-pink {
        background-color: #f6a4b9;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .highlight-blue {
        background-color: #2e35a0;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .post-box {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        border: 1px solid #f6a4b9;
    }
</style>
""", unsafe_allow_html=True)

# Title and Info
st.title("Shortlisted Influencers for Outreach")

if "shortlisted_influencers" not in st.session_state or not st.session_state.shortlisted_influencers:
    st.warning("No influencers shortlisted yet. Go back to the List Page to select influencers.")
    st.stop()

# Load influencer data again (you can modify this part to load your data from the session if it's cached earlier)
df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)

# Filter data by shortlisted influencers
shortlisted_df = df[df['username'].isin(st.session_state.shortlisted_influencers)]

# Display influencers
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
        st.write(f"**{row['Niche']}**")
    
    with cols[5]:
        st.write(f"**Bio:** {row['bio'] if pd.notna(row['bio']) else 'No bio available'}")

    # Add a checkbox to select influencers for outreach
    selected_outreach_key = f"outreach_{row['username']}"
    if st.checkbox(f"Send DM to {row['username']}", key=selected_outreach_key):
        if "outreach_influencers" not in st.session_state:
            st.session_state.outreach_influencers = []
        if row['username'] not in st.session_state.outreach_influencers:
            st.session_state.outreach_influencers.append(row['username'])

# If there are influencers selected for outreach, show a button to proceed to outreach page
if "outreach_influencers" in st.session_state and st.session_state.outreach_influencers:
    st.markdown("---")
    st.write(f"**Selected for Outreach:** {len(st.session_state.outreach_influencers)} influencers.")
    st.button("Proceed to Outreach Page", on_click=lambda: st.session_state.page = 'outreach')

# Go to Outreach Page button on top right
st.sidebar.button("Go to Outreach Page", on_click=lambda: st.session_state.page = 'outreach')
