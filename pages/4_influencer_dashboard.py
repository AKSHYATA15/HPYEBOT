import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Load Instagram data
    df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)

    # Load YouTube data
    yt = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=1)
    yt = yt.rename(columns={"instagram_username": "username"})
    
    df = pd.merge(df, yt[["username", "subscribers"]], on="username", how="left")
    df["max_audience"] = df[["followers", "subscribers"]].max(axis=1)

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

# Set page config
st.set_page_config(page_title="Influencer Dashboard", layout="wide")

# Read URL parameters
query_params = st.query_params
username = query_params.get("username", [None])[0]
niche = query_params.get("niche", [None])[0]
infl_type = query_params.get("influencer_type", [None])[0]

# Validation
if not username:
    st.error("No influencer selected.")
    st.stop()

# Filter for the influencer
influencer_data = df[df["username"] == username]

if influencer_data.empty:
    st.warning("Influencer not found.")
    st.stop()

# Extract first row
row = influencer_data.iloc[0]

# Header
st.title(f"📊 {row['username']}'s Dashboard")

# Profile picture and basic info
cols = st.columns([1, 3, 2])
with cols[0]:
    if pd.notna(row["profile_pic_url"]):
        st.image(row["profile_pic_url"], width=100)
    else:
        st.image("https://via.placeholder.com/100", width=100)

with cols[1]:
    st.markdown(f"**Niche**: {row['Niche']}")
    st.markdown(f"**Type**: {row['Influencer_Type']}")

with cols[2]:
    st.metric("Instagram Followers", f"{int(row['followers']):,}" if not pd.isna(row['followers']) else "N/A")
    if pd.notna(row['subscribers']):
        st.metric("YouTube Subscribers", f"{int(row['subscribers']):,}")

# You can continue adding more visualizations and metrics below...
