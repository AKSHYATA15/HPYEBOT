# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from pathlib import Path

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Search Influencers", 
    layout="wide", 
    page_icon="🔍",
    initial_sidebar_state="expanded"
)

# Responsive CSS
def inject_custom_css():
    st.markdown("""
    <style>
        :root {
            --primary: #4A80F0;
            --secondary: #8E2DE2;
            --dark: #1A1A1A;
            --light: #F8F9FA;
        }
        
        /* Responsive text sizing */
        html {
            font-size: 16px;
        }
        @media (max-width: 768px) {
            html {
                font-size: 14px;
            }
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            font-size: 0.95rem !important;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        /* Layout adjustments */
        .stContainer {
            max-width: 100% !important;
            padding: 0 1rem !important;
        }
        
        /* Header responsive */
        .header-title {
            font-size: 2rem !important;
            line-height: 1.2 !important;
        }
        @media (max-width: 768px) {
            .header-title {
                font-size: 1.5rem !important;
            }
        }
        
        /* Card responsive */
        .feature-card {
            padding: 1rem !important;
        }
        
        /* Column adjustments */
        @media (max-width: 768px) {
            .stColumn {
                min-width: 100% !important;
            }
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

# Initialize
inject_custom_css()
df = load_data()

# --- Hero Section ---
st.markdown("""
<div style="background: linear-gradient(90deg, #4A80F0, #8E2DE2);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            color: white;">
    <h1 class="header-title">🔍 Discover Premium Influencers</h1>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">
        Find the perfect creators across Instagram and YouTube for your brand
    </p>
</div>
""", unsafe_allow_html=True)

# --- Niche Selection ---
st.subheader("✨ Select Your Niche")
st.caption("Choose a category to find relevant influencers")

niches = df["Niche"].dropna().unique().tolist()
cols = st.columns(min(3, len(niches)))  # Responsive column count
for i, niche in enumerate(niches):
    with cols[i % len(cols)]:
        if st.button(niche, key=f"niche_{i}"):
            st.session_state["selected_niche"] = niche

# --- Influencer Type Selection ---
if "selected_niche" in st.session_state:
    st.markdown("---")
    st.subheader(f"🎯 Select Influencer Tier")
    st.caption(f"Available tiers for {st.session_state['selected_niche']} niche")
    
    influencer_types = df[df["Niche"] == st.session_state["selected_niche"]]["Influencer_Type"].unique()
    type_cols = st.columns(min(4, len(influencer_types)))  # Responsive column count
    
    for i, infl_type in enumerate(influencer_types):
        with type_cols[i % len(type_cols)]:
            if st.button(infl_type, key=f"type_{i}"):
                st.session_state["selected_category"] = infl_type
                st.switch_page("pages/3_list_page.py")

# --- Platform Stats ---
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

# --- How It Works ---
st.markdown("---")
with st.expander("💡 How To Find Influencers", expanded=True):
    st.markdown("""
    1. **Select a Niche** - Choose your industry or content category
    2. **Choose Influencer Tier** - Pick based on audience size
    3. **View Results** - Explore matching influencer profiles
    
    Our platform combines data from both Instagram and YouTube to give you
    the most comprehensive influencer discovery experience.
    """)

# Responsive empty state
if "selected_niche" not in st.session_state:
    st.markdown("---")
    st.info("👈 Please select a niche to begin your search")
