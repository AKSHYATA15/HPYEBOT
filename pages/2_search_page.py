# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Search Influencers", 
    layout="wide", 
    page_icon="🔍",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    st.markdown("""
    <style>
        :root {
            --primary: #4A80F0;
            --secondary: #8E2DE2;
            --dark: #1A1A1A;
            --light: #F8F9FA;
        }
        html {
            font-size: 17px;
        }
        @media (max-width: 768px) {
            html {
                font-size: 15px;
            }
        }
        .stButton>button {
            border-radius: 10px !important;
            padding: 0.85rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #4A80F0, #8E2DE2);
            color: white;
        }
        .niche-btn {
            background: linear-gradient(135deg, #FFC371, #FF5F6D);
            color: white;
            border-radius: 8px;
            font-weight: bold;
            padding: 0.6rem 1.2rem;
            font-size: 0.95rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .niche-btn:hover {
            background: linear-gradient(135deg, #FF5F6D, #FFC371);
            transform: scale(1.05);
        }
        .header-title {
            font-size: 2.5rem !important;
            font-weight: 800;
        }
        .platform-metric {
            font-size: 2rem;
            font-weight: 700;
        }
        .expander-header p {
            font-size: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)
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

inject_custom_css()
df = load_data()

st.markdown("""
<div style="background: linear-gradient(90deg, #4A80F0, #8E2DE2);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            color: white;">
    <h1 class="header-title">🔍 Discover Premium Influencers</h1>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.15rem;">
        Find the perfect creators across Instagram and YouTube for your brand
    </p>
</div>
""", unsafe_allow_html=True)

st.subheader("🌟 Select Your Niche")
st.caption("Choose a category to find relevant influencers")

niches = df["Niche"].dropna().unique().tolist()
cols = st.columns(3)
for i, niche in enumerate(niches):
    with cols[i % 3]:
        if st.button(niche, key=f"niche_{i}"):
            st.session_state["selected_niche"] = niche

if "selected_niche" in st.session_state:
    st.markdown("---")
    st.subheader(f"🎯 Select Influencer Tier")
    st.caption(f"Available tiers for {st.session_state['selected_niche']} niche")

    influencer_types = df[df["Niche"] == st.session_state["selected_niche"]]["Influencer_Type"].unique()
    type_cols = st.columns(min(4, len(influencer_types)))

    for i, infl_type in enumerate(influencer_types):
        with type_cols[i % len(type_cols)]:
            if st.button(infl_type, key=f"type_{i}"):
                st.session_state["selected_category"] = infl_type
                st.switch_page("pages/3_list_page.py")

st.markdown("---")
st.subheader("📊 Platform Overview")
platform_cols = st.columns(2)

with platform_cols[0]:
    st.metric("Instagram Influencers", 
              value=f"{len(df[df['followers'].notna()]):,}",
              help="Creators with Instagram profiles")

with platform_cols[1]:
    st.metric("YouTube Creators", 
              value=f"{len(df[df['subscribers'].notna()]):,}",
              help="Creators with YouTube channels")

st.markdown("---")
with st.expander("💡 How To Find Influencers", expanded=True):
    st.markdown("""
    1. **Select a Niche** - Choose your industry or content category  
    2. **Choose Influencer Tier** - Pick based on audience size  
    3. **View Results** - Explore matching influencer profiles  

    Our platform combines data from both Instagram and YouTube to give you
    the most comprehensive influencer discovery experience.
    """)

if "selected_niche" not in st.session_state:
    st.markdown("---")
    st.info("👈 Please select a niche to begin your search")
