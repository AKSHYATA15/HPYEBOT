import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)
    yt = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=1)
    yt = yt.rename(columns={"instagram_username": "username"})
    df = pd.merge(df, yt[["username", "subscribers", "video_views"]], on="username", how="left")
    return df[df["status"] == "Success"]

df = load_data()

# 🔑 Get the username from query params
query_params = st.query_params if hasattr(st, 'query_params') else st.experimental_get_query_params()
username = query_params.get("username", [None])[0]

if not username:
    st.error("No influencer selected. Please go back to the list.")
    st.stop()

user = df[df["username"] == username]
if user.empty:
    st.error("Influencer not found.")
    st.stop()

# ---- DASHBOARD UI ----
st.set_page_config(page_title=f"{username} Dashboard", layout="wide")
st.title(f"📊 {username} Dashboard")

row = user.iloc[0]
col1, col2 = st.columns([1, 3])

with col1:
    if pd.notna(row["profile_pic_url"]):
        st.image(row["profile_pic_url"], width=120)
    else:
        st.image("https://via.placeholder.com/120", width=120)

with col2:
    st.markdown(f"**Bio:** {row['bio']}")
    st.markdown(f"**Niche:** {row['Niche']}")

st.markdown("---")
st.subheader("📱 Instagram Metrics")
st.metric("Followers", f"{int(row['followers']):,}")
st.metric("Posts", f"{int(row['posts_count'])}" if not pd.isna(row['posts_count']) else "N/A")

if not pd.isna(row.get("engagement")):
    st.metric("Engagement Rate", f"{row['engagement']:.2f}%")
else:
    # You can also calculate engagement rate from likes/comments if data available
    st.write("Engagement Rate: N/A")

st.markdown("---")
st.subheader("▶️ YouTube Metrics")
if pd.notna(row["subscribers"]):
    st.metric("Subscribers", f"{int(row['subscribers']):,}")
    if pd.notna(row.get("video_views")):
        st.metric("Total Views", f"{int(row['video_views']):,}")
else:
    st.write("No YouTube data available.")
