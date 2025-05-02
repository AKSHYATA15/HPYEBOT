# Main metrics in tabs
tab1, tab2 = st.tabs(["📊 Instagram", "▶️ YouTube"])

# Update style for increasing font size
st.markdown("""
    <style>
        .stMetric {font-size: 18px;}
        .stSubheader {font-size: 20px;}
        .stTextInput, .stTextArea {font-size: 16px;}
        .stButton {font-size: 16px;}
        .stMarkdown {font-size: 18px;}
        .stTitle {font-size: 24px;}
        .stCaption {font-size: 16px;}
    </style>
""", unsafe_allow_html=True)

# Profile image and bio
with tab1:
    cols = st.columns(2)
    with cols[0]:
        st.image(row.get("youtube_profile_image") or row.get("profile_pic_url") or "https://via.placeholder.com/100", width=120)
    with cols[1]:
        st.markdown(f"**{row['username']}**", unsafe_allow_html=True)
        st.caption(row.get("bio", "No bio available"))

    # Instagram Metrics
    st.subheader("Instagram Metrics")
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
        # Calculate engagement rate (standard industry formula)
        avg_likes = (row["most_liked_likes"] + row["least_liked_likes"]) / 2
        avg_comments = (row["most_liked_comments"] + row["least_liked_comments"]) / 2
        eng_rate = ((avg_likes + avg_comments) / row["followers"]) * 100
        st.metric("Engagement Rate", f"{eng_rate:.2f}%", help="Standard formula: (Avg Likes + Avg Comments) / Followers × 100")
    except Exception as e:
        st.warning(f"Could not calculate engagement rate: {str(e)}")

    # Top Posts
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
    # YouTube Metrics
    if pd.notna(row.get('subscribers')):
        st.subheader("YouTube Analytics")
        if pd.notna(row.get('profile_link')):
            st.markdown(f"**YouTube Channel:** [View Profile]({row['profile_link']})")
        else:
            st.markdown("**YouTube Channel:** Link not available")

        # YouTube metrics in columns
        cols = st.columns(3)
        with cols[0]:
            st.metric("Subscribers", f"{int(row['subscribers']):,}")
        with cols[1]:
            st.metric("Total Views", f"{int(row['total_views']):,}")

        # Top video section
        st.markdown("**Top Performing Video**")
        st.markdown(f"[View on YouTube]({row.get('top_video_link', '#')})")
        st.metric("Views", f"{int(row['top_video_views']):,}")
    else:
        st.info("No YouTube data available for this influencer")

# Increase font size for username and dashboard elements in the influencer list
st.markdown("""
    <style>
        .username {font-size: 18px; font-weight: bold;}
        .metric-box {font-size: 16px;}
    </style>
""", unsafe_allow_html=True)

# Display influencer list with increased font size
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
        st.markdown(f"**{row['username']}**", unsafe_allow_html=True)
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
                # Dashboard content
                header_image = row.get("youtube_profile_image") or row.get("profile_pic_url") or "https://via.placeholder.com/100"
                st.image(header_image, width=100)
                st.markdown(f"<h2>{row['username']}'s Dashboard</h2>", unsafe_allow_html=True)
                st.caption(row.get("bio", "No bio available"))
                st.subheader("Instagram Profile")
                st.metric("Followers", f"{int(row['followers']):,}" if pd.notna(row['followers']) else "N/A")
                st.metric("Following", f"{int(row['following']):,}" if pd.notna(row['following']) else "N/A")
                st.metric("Verified", "Yes" if row.get('is_verified', False) else "No")
                st.metric("Business Account", "Yes" if row.get('is_business_account', False) else "No")
                
                insta_profile_url = f"https://instagram.com/{row['username']}"
                st.markdown(f"**Instagram Profile:** [@{row['username']}]({insta_profile_url})")
