import streamlit as st
import pandas as pd
import random

# Load CSV
df = pd.read_csv("data/tiktok_influencers_by_hashtag - tiktok_influencers_by_hashtag.csv")

# Clean column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Setup Streamlit page
st.set_page_config(page_title="TikTok Influencer Search", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .influencer-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        box-shadow: 0 2px 6px rgba(0,0,0,0.07);
    }
    .profile-img {
        height: 60px;
        width: 60px;
        border-radius: 50%;
        font-size: 24px;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 1rem;
        font-weight: bold;
        flex-shrink: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.title("🎯 TikTok Influencer Discovery")

# Niche Filter
st.subheader("Filter by Hashtag (Niche)")
niches = df['hashtag'].dropna().unique().tolist()
selected_niche = st.multiselect("Select Niche(s):", niches, default=niches[:3])

# Followers Filter
min_followers = int(df['followers'].min())
max_followers = int(df['followers'].max())
follower_range = st.slider("Follower Range", min_followers, max_followers, (min_followers, max_followers), step=1000)

# Filter Logic
filtered_df = df[
    df['hashtag'].isin(selected_niche) &
    (df['followers'] >= follower_range[0]) &
    (df['followers'] <= follower_range[1])
]

# Avatar Generator
def initials_avatar(username):
    initials = ''.join([w[0] for w in username.strip().split()[:2]]).upper()
    colors = ['#EF476F', '#FFD166', '#06D6A0', '#118AB2', '#8338EC']
    color = random.choice(colors)
    return f'<div class="profile-img" style="background-color: {color};">{initials}</div>'

# Display Results
st.markdown("### Influencers Found")

for _, row in filtered_df.iterrows():
    avatar_html = initials_avatar(row['username'])
    bio = row['bio'] if pd.notna(row['bio']) else "No bio available"
    st.markdown(f"""
    <div class="influencer-card">
        {avatar_html}
        <div>
            <div style="font-size: 20px; font-weight: bold;">{row['username']}</div>
            <div><strong>Followers:</strong> {row['followers']:,}</div>
            <div><strong>Total Likes:</strong> {row['total_likes']:,}</div>
            <div><strong>Hashtag:</strong> {row['hashtag']}</div>
            <div><strong>Bio:</strong> {bio}</div>
            <div><a href="{row['profile_url']}" target="_blank">🔗 View Profile</a></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Empty message
if filtered_df.empty:
    st.warning("No influencers match your selected filters.")
