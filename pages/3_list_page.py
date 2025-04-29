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

# Then load your data and other components
@st.cache_data
def load_data():
    # Load Instagram data
    df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)

    # Load YouTube data
    yt = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=1)
    yt = yt.rename(columns={"instagram_username": "username"})

    # Merge YouTube with Instagram on username
    df = pd.merge(df, yt[["username", "subscribers"]], on="username", how="left")

    # Calculate max audience
    df["max_audience"] = df[["followers", "subscribers"]].max(axis=1)

    # Classify influencer type
    def classify_influencer(count):
        if count < 10_000:
            return "Nano"
        elif count < 100_000:
            return "Micro"
        elif count < 500_000:
            return "Mid-Tier"
        elif count < 1_000_000:
            return "Macro"
        elif count < 5_000_000:
            return "Mega"
        else:
            return "Celebrity"

    df["Influencer_Type"] = df["max_audience"].apply(classify_influencer)
    return df[df["status"] == "Success"]

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
            image_url = row.get("profile_pic_url")
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
            
            # Create a popup button for the dashboard
            if st.button("View Dashboard", key=f"view_more_{row['username']}"):
                # Create a popup with all dashboard metrics
                with st.popover(f"📊 {row['username']}'s Dashboard", use_container_width=True):
                    # Header Section
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.image(row["profile_pic_url"] if pd.notna(row["profile_pic_url"]) else 
                                "https://via.placeholder.com/100", width=100)
                    with col2:
                        st.markdown(f"<h1 class='header'>📊 {row['username']}'s Dashboard</h1>", 
                                   unsafe_allow_html=True)
                    
                    # Basic Info Section
                    with st.container():
                        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                        cols = st.columns(3)
                        with cols[0]:
                            st.markdown(f"<div class='highlight-pink'>👤 Bio</div>", unsafe_allow_html=True)
                            st.markdown(f"{row['bio']}")
                        with cols[1]:
                            st.markdown(f"<div class='highlight-pink'>🏷️ Niche</div>", unsafe_allow_html=True)
                            st.markdown(f"{row['Niche']}")
                        with cols[2]:
                            st.markdown(f"<div class='highlight-pink'>📂 Category</div>", unsafe_allow_html=True)
                            st.markdown(f"{row['category_name']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Metrics Section
                    with st.container():
                        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                        cols = st.columns(4)
                        with cols[0]:
                            st.markdown(f"<div class='highlight-blue'>👥 Followers</div>", unsafe_allow_html=True)
                            st.markdown(f"**{int(row['followers']):,}**")
                        with cols[1]:
                            st.markdown(f"<div class='highlight-blue'>👤 Following</div>", unsafe_allow_html=True)
                            st.markdown(f"**{int(row['following']):,}**")
                        with cols[2]:
                            st.markdown(f"<div class='highlight-blue'>✅ Verified</div>", unsafe_allow_html=True)
                            st.markdown(f"**{'Yes' if row['is_verified'] else 'No'}**")
                        with cols[3]:
                            st.markdown(f"<div class='highlight-blue'>🏢 Business</div>", unsafe_allow_html=True)
                            st.markdown(f"**{'Yes' if row['is_business_account'] else 'No'}**")
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Engagement Metrics
                    try:
                        avg_likes = (row["most_liked_likes"] + row["least_liked_likes"]) / 2
                        avg_comments = (row["most_liked_comments"] + row["least_liked_comments"]) / 2
                        eng_rate = ((avg_likes + avg_comments) / row["followers"]) * 100
                    except:
                        eng_rate = 0

                    with st.container():
                        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                        cols = st.columns(2)
                        with cols[0]:
                            st.markdown(f"<div class='highlight-pink'>📈 Engagement Rate</div>", unsafe_allow_html=True)
                            st.markdown(f"**{eng_rate:.2f}%**")
                        with cols[1]:
                            st.markdown(f"<div class='highlight-pink'>🌟 Influencer Type</div>", unsafe_allow_html=True)
                            st.markdown(f"**{row['Influencer_Type']}**")
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Post Previews
                    st.markdown("<h2 class='header'>📸 Post Performance</h2>", unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown('<div class="post-box">', unsafe_allow_html=True)
                        st.markdown(f"<div class='highlight-blue'>🔥 Most Liked Post</div>", unsafe_allow_html=True)
                        st.markdown(f"[View on Instagram]({row['most_liked_url']})")
                        cols = st.columns(2)
                        with cols[0]:
                            st.markdown(f"❤️ **{int(row['most_liked_likes']):,}** likes")
                        with cols[1]:
                            st.markdown(f"💬 **{int(row['most_liked_comments']):,}** comments")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.container():
                        st.markdown('<div class="post-box">', unsafe_allow_html=True)
                        st.markdown(f"<div class='highlight-blue'>💤 Least Liked Post</div>", unsafe_allow_html=True)
                        st.markdown(f"[View on Instagram]({row['least_liked_url']})")
                        cols = st.columns(2)
                        with cols[0]:
                            st.markdown(f"❤️ **{int(row['least_liked_likes']):,}** likes")
                        with cols[1]:
                            st.markdown(f"💬 **{int(row['least_liked_comments']):,}** comments")
                        st.markdown('</div>', unsafe_allow_html=True)

                    # YouTube Section (if available)
                    if pd.notna(row['subscribers']):
                        st.markdown("<h2 class='header'>▶️ YouTube Overview</h2>", unsafe_allow_html=True)
                        
                        with st.container():
                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                            cols = st.columns([1, 4])
                            with cols[0]:
                                st.image(row["youtube_profile_image"] if pd.notna(row["youtube_profile_image"]) else 
                                        "https://via.placeholder.com/100", width=100)
                            with cols[1]:
                                st.markdown(f"<div class='highlight-pink'>📺 YouTube Name</div>", unsafe_allow_html=True)
                                st.markdown(f"**{row['youtube_name']}**")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with st.container():
                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                            cols = st.columns(3)
                            with cols[0]:
                                st.markdown(f"<div class='highlight-blue'>👥 Subscribers</div>", unsafe_allow_html=True)
                                st.markdown(f"**{int(row['subscribers']):,}**")
                            with cols[1]:
                                st.markdown(f"<div class='highlight-blue'>👀 Total Views</div>", unsafe_allow_html=True)
                                st.markdown(f"**{int(row['total_views']):,}**")
                            with cols[2]:
                                st.markdown(f"<div class='highlight-blue'>🎥 Top Video</div>", unsafe_allow_html=True)
                                st.markdown(f"[View Video]({row['top_video_link']}) ({int(row['top_video_views']):,} views)")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with st.container():
                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                            cols = st.columns(2)
                            with cols[0]:
                                try:
                                    yt_engagement = (row["top_video_views"] / row["subscribers"]) * 100
                                    st.markdown(f"<div class='highlight-pink'>📊 YouTube Engagement</div>", unsafe_allow_html=True)
                                    st.markdown(f"**{yt_engagement:.2f}%**")
                                except:
                                    st.markdown(f"<div class='highlight-pink'>📊 YouTube Engagement</div>", unsafe_allow_html=True)
                                    st.markdown("**N/A**")
                            with cols[1]:
                                max_reach = max(row["followers"], row["subscribers"])
                                st.markdown(f"<div class='highlight-pink'>🌐 Combined Influencer Type</div>", unsafe_allow_html=True)
                                st.markdown(f"**{row['Influencer_Type']}**")
                            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()
