import streamlit as st
import pandas as pd
import random
import hashlib

# Load data
df = pd.read_csv("data/tiktok_influencers_by_hashtag - tiktok_influencers_by_hashtag.csv")

# Preprocess columns (rename for consistency)
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Sidebar customization
st.set_page_config(page_title="TikTok Influencer Search", layout="wide")
st.markdown("""
    <style>
    .css-1d391kg {padding-top: 1rem;}
    .influencer-card {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
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
    }
    </style>
""", unsafe_allow_html=True)

st.title("📱 TikTok Influencer Discovery")

# Niche filter
st.subheader("Search by Niche")
niches = df['Hashtag'].dropna().unique().tolist()
selected_niche = st.multiselect("Select niche(s):", niches, default=niches[:3])

# Followers filter
min_followers = int(df['Followers'].min())
max_followers = int(df['Followers'].max())
follower_range = st.slider("Select follower range:", min_followers, max_followers, (min_followers, max_followers), step=1000)

# Filter logic
filtered_df = df[
    df['Hashtag'].isin(selected_niche) &
    (df['Followers'] >= follower_range[0]) &
    (df['Followers'] <= follower_range[1])
]

# Display
st.markdown("### Matching Influencers")

def initials_avatar(Username):
    initials = ''.join([w[0] for w in username.split()[:2]]).upper()
    colors = ['#EF476F', '#FFD166', '#06D6A0', '#118AB2', '#073B4C']
    color = random.choice(colors)
    return f'<div class="profile-img" style="background-color: {color};">{initials}</div>'

for _, row in filtered_df.iterrows():
    avatar_html = initials_avatar(row['Username'])
    st.markdown(f"""
    <div class="influencer-card">
        {avatar_html}
        <div>
            <div style="font-size: 20px; font-weight: bold;">{row['Username']}</div>
            <div style="font-size: 20px;">{row['Full Name']}</div>
            <div>
                <Bio :> {row['Bio']:,}</div>
                <div><Followers: {row['Followers']:,}</div>
                <div>Likes: {row.get('Total Likes', 'N/A')}</div>
            <div>Niche: {row['Hashtag']}</div>
            <div><a href="{row['Profile URL']}" target="_blank">Visit Profile</a></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if filtered_df.empty:
    st.info("No influencers found for the selected filters.")

