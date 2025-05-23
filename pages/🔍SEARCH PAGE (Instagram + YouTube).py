# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Search Influencers", 
    layout="wide", 
    page_icon="🔍",
    initial_sidebar_state="collapsed"
)

import streamlit.components.v1 as components

components.html("""
    <script>
        window.parent.scrollTo(0, 0);
    </script>
""", height=0)


def inject_custom_css():
    st.markdown("""
    <style>
        :root {
            --primary: #4A80F0;
            --secondary: #8E2DE2;
            --dark: #1A1A1A;
            --light: #F8F9FA;
        }
        html, body, div, p, span, button {
            font-size: 18px !important;
        }
        @media (max-width: 768px) {
            html {
                font-size: 16px !important;
            }
        }

        
    .main {
    background-color: #f8f9fa;
}
[data-testid="stSidebar"] {
    padding: 2.5rem 1.5rem !important;
    box-shadow: 5px 0 15px rgba(0,0,0,0.1);
}
[data-testid="stSidebarNav"] > ul {
    font-size: 1.15rem;
    gap: 12px;
}
[data-testid="stSidebarNav"] ul li {
    margin-bottom: 20px;
    font-weight: 500;
    transition: all 0.3s ease;
    padding: 8px 12px;
    border-radius: 6px;
}
[data-testid="stSidebarNav"] ul li:hover {
    background: rgba(0,0,0,0.05);
    transform: translateX(5px);
}
    
        .stButton>button {
            border-radius: 10px !important;
            padding: 0.85rem 1.5rem !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #4A80F0, #8E2DE2);
            color: white;
        }
        .header-title {
            font-size: 2.75rem !important;
            font-weight: 800;
        }
        .platform-metric {
            font-size: 2rem;
            font-weight: 700;
        }
        .expander-header p {
            font-size: 1.15rem !important;
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
    <p style="color: rgba(255,255,255,0.95); font-size: 1.25rem;">
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
                st.switch_page("pages/📋List Page.py")

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
