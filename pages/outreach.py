import streamlit as st
import time
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

# Set page config
st.set_page_config(page_title="Outreach Page", layout="wide", initial_sidebar_state="collapsed")

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

# Title
st.title("📩 Instagram DM Outreach")

if "outreach_influencers" not in st.session_state or not st.session_state.outreach_influencers:
    st.warning("No influencers selected for outreach. Please go back to the shortlist page and select some.")
    st.stop()

# Load influencer data
df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)

# Filter influencers selected for outreach
outreach_df = df[df['username'].isin(st.session_state.outreach_influencers)]

# Display selected influencers
for _, row in outreach_df.iterrows():
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

# Instagram DM functionality
st.markdown("### Send DMs to Selected Influencers")
dm_text = st.text_area("Message Text", "Hi {username}, I wanted to reach out and discuss a potential collaboration...")

if st.button("Send DMs to Selected Influencers"):
    if not dm_text.strip():
        st.warning("Please enter a message to send.")
        st.stop()

    # Authenticate and send DMs
    username = st.text_input("Instagram Username", "")
    password = st.text_input("Instagram Password", type="password")

    if username and password:
        with st.spinner("Logging in..."):
            try:
                client = Client()
                client.login(username, password)

                # Send DMs to selected influencers
                for _, row in outreach_df.iterrows():
                    recipient_username = row['username']
                    try:
                        # Send the DM with the custom message
                        message = dm_text.format(username=recipient_username)
                        client.direct_send(message, [recipient_username])
                        st.success(f"DM sent to {recipient_username}")
                    except Exception as e:
                        st.error(f"Failed to send DM to {recipient_username}: {str(e)}")

                st.success("DMs sent successfully to all selected influencers.")
            
            except (LoginRequired, ChallengeRequired):
                st.error("Login failed! Please check your credentials or authenticate the login activity.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter your Instagram credentials to log in.")
