import streamlit as st
import pandas as pd
import time
import random
import os
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

# Set page config must be FIRST command
st.set_page_config(
    page_title="Influencer List", 
    layout="wide",
    page_icon="✨"
)

# Modern, beautiful CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .header {
        color: #3A36DB;
        border-bottom: 3px solid #FF7BA9;
        padding-bottom: 15px;
        margin-bottom: 30px;
        font-weight: 700;
    }
    
    .metric-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #3A36DB;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }
    
    .highlight-pink {
        background: linear-gradient(135deg, #FF7BA9, #FF9B8A);
        color: white;
        padding: 8px 15px;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }
    
    .highlight-blue {
        background: linear-gradient(135deg, #3A36DB, #5E8BFF);
        color: white;
        padding: 8px 15px;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }
    
    .post-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        border: 2px solid #FFE5EE;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    .popover-content {
        max-height: 80vh;
        overflow-y: auto;
        padding: 20px;
        background: #F9FAFF;
    }
    
    .influencer-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .influencer-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }
    
    .profile-img {
        border-radius: 50%;
        border: 3px solid #FF7BA9;
        width: 80px;
        height: 80px;
        object-fit: cover;
    }
    
    .username-text {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2D3748;
        margin-bottom: 5px;
    }
    
    .niche-text {
        font-size: 1rem;
        color: #718096;
        font-weight: 500;
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #718096;
        font-weight: 500;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2D3748;
    }
    
    .stButton>button {
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    .dashboard-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2D3748;
        margin-bottom: 15px;
    }
    
    .tab-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #3A36DB;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2D3748;
        margin: 20px 0 10px 0;
    }
    
    @media (max-width: 768px) {
        .username-text {
            font-size: 1.2rem;
        }
        .metric-value {
            font-size: 1.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    try:
        df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)
        try:
            yt = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=1)
            yt = yt.rename(columns={"instagram_username": "username"})
            df = pd.merge(df, yt[["username", "subscribers", "total_views", "youtube_name", 
                                 "youtube_profile_image", "top_video_link", "top_video_views"]], 
                         on="username", how="left")
        except Exception as e:
            st.warning(f"Could not load YouTube data: {str(e)}")
            df["subscribers"] = None
            df["total_views"] = None
            df["youtube_name"] = None
            df["youtube_profile_image"] = None
            df["top_video_link"] = None
            df["top_video_views"] = None

        df["max_audience"] = df[["followers", "subscribers"]].max(axis=1)

        def classify_influencer(count):
            try:
                count = float(count) if not pd.isna(count) else 0
                if count < 10_000: return "Nano"
                elif count < 100_000: return "Micro"
                elif count < 500_000: return "Mid-Tier"
                elif count < 1_000_000: return "Macro"
                elif count < 5_000_000: return "Mega"
                else: return "Celebrity"
            except:
                return "Unknown"

        df["Influencer_Type"] = df["max_audience"].apply(classify_influencer)
        return df[df["status"] == "Success"]

    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        return pd.DataFrame()

df = load_data()
niche = st.session_state.get("selected_niche")
infl_type = st.session_state.get("selected_category")

if not niche or not infl_type:
    st.warning("Please select both a Niche and Influencer Type.")
    st.stop()

st.markdown(f"<h1 class='header'>✨ {niche} Influencers | {infl_type} Tier</h1>", unsafe_allow_html=True)
filtered_df = df[(df["Niche"] == niche) & (df["Influencer_Type"] == infl_type)]

if filtered_df.empty:
    st.info("No influencers found for the selected criteria.")
else:
    for _, row in filtered_df.iterrows():
        with st.container():
            st.markdown("<div class='influencer-card'>", unsafe_allow_html=True)
            
            cols = st.columns([1, 3, 2, 2, 2, 2])
            
            # Profile Image
            with cols[0]:
                image_url = row.get("youtube_profile_image", row.get("profile_pic_url"))
                profile_url = f"https://instagram.com/{row['username']}"
                if pd.notna(image_url) and pd.notna(profile_url):
                    st.markdown(f"<a href='{profile_url}'><img class='profile-img' src='{image_url}'></a>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<a href='{profile_url if pd.notna(profile_url) else '#'}'><img class='profile-img' src='https://via.placeholder.com/80'></a>", unsafe_allow_html=True)
            
            # Username and Niche
            with cols[1]:
                st.markdown(f"<div class='username-text'>@{row['username']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='niche-text'>{row['Niche']}</div>", unsafe_allow_html=True)
            
            # Instagram Followers
            with cols[2]:
                st.markdown("<div class='metric-title'>Instagram Followers</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{int(row['followers']):,}</div>" if not pd.isna(row['followers']) else "<div class='metric-value'>N/A</div>", unsafe_allow_html=True)
            
            # YouTube Subscribers
            with cols[3]:
                if pd.notna(row['subscribers']):
                    st.markdown("<div class='metric-title'>YouTube Subscribers</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='metric-value'>{int(row['subscribers']):,}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='metric-title'>YouTube</div>", unsafe_allow_html=True)
                    st.markdown("<div class='metric-value'>No Data</div>", unsafe_allow_html=True)
            
            # View Dashboard Button
            with cols[4]:
                if st.button("📊 View Dashboard", key=f"view_more_{row['username']}"):
                    with st.popover(f"✨ {row['username']}'s Dashboard", use_container_width=True):
                        header_image = row.get("youtube_profile_image") or row.get("profile_pic_url") or "https://via.placeholder.com/100"
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.image(header_image, width=100)
                        with col2:
                            st.markdown(f"<div class='dashboard-title'>{row['username']}'s Dashboard</div>", unsafe_allow_html=True)
                            st.caption(row.get("bio", "No bio available"))
                        
                        tab1, tab2 = st.tabs(["📊 Instagram Analytics", "▶️ YouTube Analytics"])
                        
                        with tab1:
                            st.markdown("<div class='tab-title'>Instagram Profile</div>", unsafe_allow_html=True)
                            cols = st.columns(2)
                            with cols[0]:
                                st.markdown("<div class='metric-title'>Followers</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='metric-value'>{int(row['followers']):,}</div>" if pd.notna(row['followers']) else "<div class='metric-value'>N/A</div>", unsafe_allow_html=True)
                                
                                st.markdown("<div class='metric-title'>Following</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='metric-value'>{int(row['following']):,}</div>" if pd.notna(row['following']) else "<div class='metric-value'>N/A</div>", unsafe_allow_html=True)
                            
                            with cols[1]:
                                st.markdown("<div class='metric-title'>Verified</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='metric-value'>{'✅ Yes' if row.get('is_verified', False) else '❌ No'}</div>", unsafe_allow_html=True)
                                
                                st.markdown("<div class='metric-title'>Business Account</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='metric-value'>{'✅ Yes' if row.get('is_business_account', False) else '❌ No'}</div>", unsafe_allow_html=True)
                            
                            insta_profile_url = f"https://instagram.com/{row['username']}"
                            st.markdown(f"**Instagram Profile:** [@{row['username']}]({insta_profile_url})")
                            
                            st.markdown("<div class='section-title'>Engagement Metrics</div>", unsafe_allow_html=True)
                            try:
                                avg_likes = (row["most_liked_likes"] + row["least_liked_likes"]) / 2
                                avg_comments = (row["most_liked_comments"] + row["least_liked_comments"]) / 2
                                eng_rate = ((avg_likes + avg_comments) / row["followers"]) * 100
                                posts_per_week = row.get("posts_per_week", 0)
                                st.metric("Engagement Rate", f"{eng_rate:.2f}%", help="Standard formula: (Avg Likes + Avg Comments) / Followers × 100")
                            except Exception as e:
                                st.warning(f"Could not calculate engagement rate: {str(e)}")
                            
                            st.markdown("<div class='section-title'>Top Posts</div>", unsafe_allow_html=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Most Liked Post**")
                                if pd.notna(row.get("most_liked_url")):
                                    st.markdown(f"[View Post]({row['most_liked_url']})")
                                    st.markdown(f"<div class='metric-value'>{int(row['most_liked_likes']):,} likes</div>", unsafe_allow_html=True)
                                else:
                                    st.info("No post data available")
                            with col2:
                                st.markdown("**Least Liked Post**")
                                if pd.notna(row.get("least_liked_url")):
                                    st.markdown(f"[View Post]({row['least_liked_url']})")
                                    st.markdown(f"<div class='metric-value'>{int(row['least_liked_likes']):,} likes</div>", unsafe_allow_html=True)
                                else:
                                    st.info("No post data available")
                        
                        with tab2:
                            if pd.notna(row.get('subscribers')):
                                st.markdown("<div class='tab-title'>YouTube Channel</div>", unsafe_allow_html=True)
                                if pd.notna(row.get('profile_link')):
                                    st.markdown(f"**YouTube Channel:** [View Profile]({row['profile_link']})")
                                else:
                                    st.markdown("**YouTube Channel:** Link not available")
                                
                                cols = st.columns(3)
                                with cols[0]:
                                    st.markdown("<div class='metric-title'>Subscribers</div>", unsafe_allow_html=True)
                                    st.markdown(f"<div class='metric-value'>{int(row['subscribers']):,}</div>", unsafe_allow_html=True)
                                with cols[1]:
                                    st.markdown("<div class='metric-title'>Total Views</div>", unsafe_allow_html=True)
                                    st.markdown(f"<div class='metric-value'>{int(row['total_views']):,}</div>", unsafe_allow_html=True)
                                
                                st.markdown("<div class='section-title'>Top Performing Video</div>", unsafe_allow_html=True)
                                st.markdown(f"[View on YouTube]({row.get('top_video_link', '#')})")
                                st.markdown(f"<div class='metric-value'>{int(row['top_video_views']):,} views</div>", unsafe_allow_html=True)
                            else:
                                st.info("No YouTube data available for this influencer")
            
            # Message Button
            with cols[5]:
                if st.button("💌 Send Message", key=f"msg_btn_{row['username']}"):
                    with st.popover(f"📩 Message @{row['username']}"):
                        with st.form(key=f"dm_form_{row['username']}"):
                            ig_username = st.text_input("Your Instagram Username")
                            ig_password = st.text_input("Your Instagram Password", type="password")
                            default_message = f"Hi @{row['username']}, I came across your profile and wanted to connect..."
                            message = st.text_area("Message", value=default_message, height=150)

                            if st.form_submit_button("Send Message"):
                                session_file = f"sessions/{ig_username}_session.json"
                                try:
                                    cl = Client()
                                    cl.delay_range = [1, 3]

                                    if os.path.exists(session_file):
                                        cl.load_settings(session_file)
                                        cl.login(ig_username, ig_password)
                                    else:
                                        cl.login(ig_username, ig_password)
                                        os.makedirs("sessions", exist_ok=True)
                                        cl.dump_settings(session_file)

                                    user_id = cl.user_id_from_username(row['username'])
                                    time.sleep(random.uniform(1, 2))
                                    cl.direct_send(message, user_ids=[user_id])
                                    time.sleep(random.uniform(2, 4))
                                    st.success(f"✅ Message sent to @{row['username']}")
                                    st.balloons()

                                except ChallengeRequired:
                                    st.error("🔐 Verification required - please login via mobile first")
                                except Exception as e:
                                    st.error(f"❌ Failed to send message: {str(e)}")
                                finally:
                                    try:
                                        cl.logout()
                                    except:
                                        pass
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.divider()
