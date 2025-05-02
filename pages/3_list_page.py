# -*- coding: utf-8 -*-
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

# CSS styling to improve frontend appearance
st.markdown("""
<style>
    .header {
        color: #2e35a0;
        font-size: 36px;
        border-bottom: 2px solid #f6a4b9;
        padding-bottom: 20px;
        font-weight: bold;
    }
    .metric-box {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 6px solid #2e35a0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        font-size: 18px;
    }
    .highlight-pink {
        background-color: #f6a4b9;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 16px;
    }
    .highlight-blue {
        background-color: #2e35a0;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 16px;
    }
    .post-box {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #f6a4b9;
        font-size: 18px;
    }
    .popover-content {
        max-height: 80vh;
        overflow-y: auto;
        padding: 20px;
    }
    h2, h3, h4 {
        font-size: 24px;
    }
    .tabs {
        font-size: 20px;
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

st.title(f"📋 Influencers - {niche} | {infl_type}")
filtered_df = df[(df["Niche"] == niche) & (df["Influencer_Type"] == infl_type)]

if filtered_df.empty:
    st.info("No influencers found for the selected criteria.")
else:
    for _, row in filtered_df.iterrows():
        cols = st.columns(6)
        with cols[0]:
            image_url = row.get("youtube_profile_image", row.get("profile_pic_url"))
            profile_url = f"https://instagram.com/{row['username']}"
            if pd.notna(image_url) and pd.notna(profile_url):
                st.markdown(f"[![profile]({image_url})]({profile_url})", unsafe_allow_html=True)
            else:
                st.markdown(f"[![profile](https://via.placeholder.com/60)]({profile_url if pd.notna(profile_url) else '#'})", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"**{row['username']}**")
        with cols[2]:
            st.metric("Instagram Followers", f"{int(row['followers']):,}" if not pd.isna(row['followers']) else "N/A")
        with cols[3]:
            if pd.notna(row['subscribers']):
                st.metric("YouTube Subscribers", f"{int(row['subscribers']):,}")
            else:
                st.write("No YouTube data")
        with cols[4]:
            st.write(f"**{row['Niche']}**")
            if st.button("View Dashboard", key=f"view_more_{row['username']}"):
                with st.popover(f"📊 {row['username']}'s Dashboard", use_container_width=True):
                    # Dashboard content without nested columns
                    header_image = row.get("youtube_profile_image") or row.get("profile_pic_url") or "https://via.placeholder.com/100"
                    st.image(header_image, width=100)
                    st.markdown(f"<h2>{row['username']}'s Dashboard</h2>", unsafe_allow_html=True)
                    st.caption(row.get("bio", "No bio available"))
                    
                    # Using tabs for Instagram and YouTube Analytics
                    tabs = st.radio("Analytics", ("Instagram", "YouTube"), key=f"analytics_tabs_{row['username']}")
                    
                    if tabs == "Instagram":
                        st.subheader("Instagram Analytics")
                        st.metric("Followers", f"{int(row['followers']):,}" if pd.notna(row['followers']) else "N/A")
                        st.metric("Following", f"{int(row['following']):,}" if pd.notna(row['following']) else "N/A")
                        st.metric("Verified", "Yes" if row.get('is_verified', False) else "No")
                        st.metric("Business Account", "Yes" if row.get('is_business_account', False) else "No")
                        
                        insta_profile_url = f"https://instagram.com/{row['username']}"
                        st.markdown(f"**Instagram Profile:** [@{row['username']}]({insta_profile_url})")
                        
                        st.subheader("Engagement")
                        try:
                            avg_likes = (row["most_liked_likes"] + row["least_liked_likes"]) / 2
                            avg_comments = (row["most_liked_comments"] + row["least_liked_comments"]) / 2
                            eng_rate = ((avg_likes + avg_comments) / row["followers"]) * 100
                            posts_per_week = row.get("posts_per_week", 0)
                            st.metric("Engagement Rate", f"{eng_rate:.2f}%", help="Standard formula: (Avg Likes + Avg Comments) / Followers × 100")
                        except Exception as e:
                            st.warning(f"Could not calculate engagement rate: {str(e)}")
                        
                        st.subheader("Top Posts")
                        st.markdown("**Most Liked Post**")
                        if pd.notna(row.get("most_liked_url")):
                            st.markdown(f"[View Post]({row['most_liked_url']})")
                            st.metric("Likes", f"{int(row['most_liked_likes']):,}")
                        else:
                            st.info("No post data available")
                        
                        st.markdown("**Least Liked Post**")
                        if pd.notna(row.get("least_liked_url")):
                            st.markdown(f"[View Post]({row['least_liked_url']})")
                            st.metric("Likes", f"{int(row['least_liked_likes']):,}")
                        else:
                            st.info("No post data available")

                    elif tabs == "YouTube":
                        st.subheader("YouTube Analytics")
                        if pd.notna(row.get('subscribers')):
                            if pd.notna(row.get('profile_link')):
                                st.markdown(f"**YouTube Channel:** [View Profile]({row['profile_link']})")
                            else:
                                st.markdown("**YouTube Channel:** Link not available")
                            
                            st.metric("Subscribers", f"{int(row['subscribers']):,}")
                            st.metric("Total Views", f"{int(row['total_views']):,}")
                            
                            st.markdown("**Top Performing Video**")
                            st.markdown(f"[View on YouTube]({row.get('top_video_link', '#')})")
                            st.metric("Views", f"{int(row['top_video_views']):,}")
                        else:
                            st.info("No YouTube data available for this influencer")

        with cols[5]:
            if st.button("💬 Message", key=f"msg_btn_{row['username']}"):
                with st.popover(f"Send DM to @{row['username']}"):
                    with st.form(key=f"dm_form_{row['username']}"):
                        ig_username = st.text_input("Your Instagram Username")
                        ig_password = st.text_input("Your Instagram Password", type="password")
                        default_message = f"Hi @{row['username']}, I came across your profile and wanted to connect..."
                        message = st.text_area("Message", value=default_message)

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
        st.divider()
                             
