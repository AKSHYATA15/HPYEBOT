
import streamlit as st
import pandas as pd
import random

# Load and clean CSV
df = pd.read_csv("data/tiktok_influencers_by_hashtag - tiktok_influencers_by_hashtag.csv")
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Set page config
st.set_page_config(page_title="TikTok Influencer Search", layout="wide",initial_sidebar_state="collapsed")

# Custom CSS
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
    .main-title {
        font-size: 40px !important;
        font-weight: 900;
        color: #202124;
        padding-top: 20px;
        padding-bottom: 10px;
    }
    .sub-header {
        font-size: 24px !important;
        font-weight: 700;
        margin-bottom: 12px;
        color: #333333;
    }
    .influencer-card {
        background-color: #f1f3f4;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: flex-start;
        box-shadow: 0 4px 10px rgba(0,0,0,0.07);
    }
    .profile-img {
        height: 72px;
        width: 72px;
        border-radius: 50%;
        font-size: 28px;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 1.5rem;
        font-weight: bold;
        flex-shrink: 0;
    }
    .slider-container .stSlider {
        max-width: 500px !important;
    }
    .info-text {
        font-size: 20px;
        line-height: 1.6;
        color: #111827;
    }
    .username {
        font-size: 24px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 0.3rem;
    }
    </style>
""", unsafe_allow_html=True)




# Title
st.markdown('<div class="main-title">🎯 TikTok Influencer Discovery</div>', unsafe_allow_html=True)

# Filters
st.markdown('<div class="sub-header">🔍 Filter by Niche</div>', unsafe_allow_html=True)
niches = sorted(df['hashtag'].dropna().unique())
selected_niche = st.selectbox("Select Niche:", niches)

# Follower filter
min_followers = int(df['followers'].min())
max_followers = int(df['followers'].max())
st.markdown('<div class="sub-header">📊 Follower Range</div>', unsafe_allow_html=True)
follower_range = st.slider("",
                           min_value=min_followers,
                           max_value=max_followers,
                           value=(min_followers, max_followers),
                           key="follower_slider")

# Filter dataset
filtered = df[
    (df['hashtag'] == selected_niche) &
    (df['followers'] >= follower_range[0]) &
    (df['followers'] <= follower_range[1])
]

# Display Results
st.markdown('<div class="sub-header">📋 Influencers Found</div>', unsafe_allow_html=True)

if filtered.empty:
    st.warning("No influencers match your selected filters.")
else:
    for _, row in filtered.iterrows():
        if pd.isna(row['username']) or not isinstance(row['username'], str):
            initials = "??"  # Set default initials if username is missing or not a string
        else:
            initials = row['username'][:2].upper()

        
        colors = ["#6366F1", "#10B981", "#EF4444", "#F59E0B", "#3B82F6", "#EC4899"]
        color = random.choice(colors)

        col1, col2 = st.columns([1, 8])
        with col1:
            st.markdown(
                f'<div class="profile-img" style="background-color: {color};">{initials}</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(f'<div class="username">{row["username"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-text">Followers: {int(row["followers"]):,}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-text">Total Likes: {int(row["total_likes"]):,}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-text">Hashtag: #{row["hashtag"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-text">Bio: {row["bio"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-text">🔗 <a href="{row["profile_url"]}" target="_blank">Visit Profile</a></div>', unsafe_allow_html=True)

