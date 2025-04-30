import streamlit as st
import pandas as pd

# Set page config must be FIRST command
st.set_page_config(page_title="Influencer List", layout="wide")

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
    .popover-content {
        max-height: 80vh;
        overflow-y: auto;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    try:
        # Load Instagram data
        df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)
        
        # Load YouTube data - added more robust error handling
        try:
            yt = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=1)
            yt = yt.rename(columns={"instagram_username": "username"})
            
            
            
            # Merge YouTube data
            df = pd.merge(df, yt[["username", "subscribers", "total_views", "youtube_name", 
                                 "youtube_profile_image", "top_video_link", "top_video_views"]], 
                         on="username", how="left")
            
            
            
        except Exception as e:
            st.warning(f"Could not load YouTube data: {str(e)}")
            # Add empty YouTube columns if merge fails
            df["subscribers"] = None
            df["total_views"] = None
            df["youtube_name"] = None
            df["youtube_profile_image"] = None
            df["top_video_link"] = None
            df["top_video_views"] = None
            
        # Calculate max audience
        df["max_audience"] = df[["followers", "subscribers"]].max(axis=1)
        
        # Classify influencer type with proper error handling
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

# Get filters from session state
niche = st.session_state.get("selected_niche")
infl_type = st.session_state.get("selected_category")

if not niche or not infl_type:
    st.warning("Please select both a Niche and Influencer Type.")
    st.stop()

st.title(f"📋 Influencers - {niche} | {infl_type}")

# Apply filters
filtered_df = df[(df["Niche"] == niche) & (df["Influencer_Type"] == infl_type)]

if filtered_df.empty:
    st.info("No influencers found for the selected criteria.")
else:
    for _, row in filtered_df.iterrows():
        cols = st.columns([1, 3, 2, 2, 2])
        with cols[0]:
            # Modified: Use YouTube profile image if available, otherwise Instagram
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
                    # Determine which profile image to use in header
                    header_image = None
                    if pd.notna(row.get("youtube_profile_image")):
                        header_image = row["youtube_profile_image"]
                    elif pd.notna(row.get("profile_pic_url")):
                        header_image = row["profile_pic_url"]
                    else:
                        header_image = "https://via.placeholder.com/100"

                    # Header Section
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.image(header_image, width=100)
                    with col2:
                        st.markdown(f"<h2>{row['username']}'s Dashboard</h2>", unsafe_allow_html=True)
                        st.caption(row.get("bio", "No bio available"))
                    
                    # Main metrics in tabs
                    tab1, tab2 = st.tabs(["📊 Instagram", "▶️ YouTube"])
                    
                    with tab1:
                        # Instagram Metrics
                        cols = st.columns(2)
                        with cols[0]:
                            st.metric("Followers", f"{int(row['followers']):,}" if pd.notna(row['followers']) else "N/A")
                            st.metric("Following", f"{int(row['following']):,}" if pd.notna(row['following']) else "N/A")
                        with cols[1]:
                            st.metric("Verified", "Yes" if row.get('is_verified', False) else "No")
                            st.metric("Business Account", "Yes" if row.get('is_business_account', False) else "No")
                        
                        # Instagram Profile Link
                        insta_profile_url = f"https://instagram.com/{row['username']}"
                        st.markdown(f"**Instagram Profile:** [@{row['username']}]({insta_profile_url})")
                        
                        # Engagement
                        st.subheader("Engagement")
                        try:
                            # Get average likes from most and least liked posts
                            avg_likes = (row["most_liked_likes"] + row["least_liked_likes"]) / 2
                            # Get average comments from most and least liked posts
                            avg_comments = (row["most_liked_comments"] + row["least_liked_comments"]) / 2
        
                            # Calculate engagement rate (standard industry formula)
                            eng_rate = ((avg_likes + avg_comments) / row["followers"]) * 100
        
                            # Additional metrics for context
                            posts_per_week = row.get("posts_per_week", 0)  # Add this column if available
                            st.metric("Engagement Rate", f"{eng_rate:.2f}%", 
                            help="Standard formula: (Avg Likes + Avg Comments) / Followers × 100")
        
                        # Contextual interpretation
        
            
                        except Exception as e:
                            st.warning(f"Could not calculate engagement rate: {str(e)}")
                        
                        # Posts - Show as links only
                        st.subheader("Top Posts")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Most Liked Post**")
                            if pd.notna(row.get("most_liked_url")):
                                st.markdown(f"[View Post]({row['most_liked_url']})")
                                st.metric("Likes", f"{int(row['most_liked_likes']):,}")
                            else:
                                st.info("No post data available")
                        
                        

                    with tab2:
                        # YouTube Metrics (only if data exists)
                        if pd.notna(row.get('subscribers')):
                            st.subheader("YouTube Analytics")
                            
                            # Add YouTube Profile Link if available
                            if pd.notna(row.get('profile_link')):
                                st.markdown(f"**YouTube Channel:** [View Profile]({row['profile_link']})")
                            
                            # YouTube metrics in columns
                            cols = st.columns(3)
                            with cols[0]:
                                st.metric("Subscribers", f"{int(row['subscribers']):,}")
                            with cols[1]:
                                st.metric("Total Views", f"{int(row['total_views']):,}")
                            with cols[2]:
                                # Calculate YouTube engagement percentage
                                try:
                                    yt_engagement = (row['total_views'] / row['subscribers']) * 100
                                    st.metric("Engagement %", f"{min(yt_engagement, 100):.2f}%") 
                                    
                                except:
                                    st.metric("Engagement %", "N/A")
                            
                            # Top video section
                            st.markdown("**Top Performing Video**")
                            st.markdown(f"[View on YouTube]({row.get('top_video_link', '#')})")
                            st.metric("Views", f"{int(row['top_video_views']):,}")
                            
                        else:
                            st.info("No YouTube data available for this influencer")

        st.divider()
