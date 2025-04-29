import streamlit as st
import pandas as pd

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

st.set_page_config(page_title="Influencer List", layout="wide")
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
            st.markdown(f"[📊 View Dashboard](?username={row['username']}&niche={row['Niche']}&influencer_type={row['Influencer_Type']})"
)

        st.divider()
