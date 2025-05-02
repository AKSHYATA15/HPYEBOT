# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from pathlib import Path

# Custom CSS for professional styling
def inject_custom_css():
    st.markdown("""
    <style>
        :root {
            --primary: #4A80F0;
            --secondary: #8E2DE2;
            --dark: #1A1A1A;
            --light: #F8F9FA;
        }
        
        .stButton>button {
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(74, 128, 240, 0.2) !important;
        }
        
        .niche-btn {
            background: white !important;
            color: var(--dark) !important;
            border: 1px solid #E0E0E0 !important;
        }
        
        .niche-btn:hover {
            border-color: var(--primary) !important;
            color: var(--primary) !important;
        }
        
        .type-btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
            color: white !important;
            border: none !important;
        }
        
        .header-container {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            color: white;
        }
        
        .platform-tag {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            margin-left: 8px;
        }
        
        .instagram-tag {
            background: #E1306C;
            color: white;
        }
        
        .youtube-tag {
            background: #FF0000;
            color: white;
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
st.set_page_config(page_title="Search Influencers", layout="wide", page_icon="🔍")

# --- Hero Section ---
st.markdown("""
<div class="header-container">
    <h1 style="color: white; margin-bottom: 0.5rem;">🔍 Discover Premium Influencers</h1>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">
        Find the perfect creators across Instagram and YouTube for your brand
    </p>
</div>
""", unsafe_allow_html=True)

# --- Search Filters ---
with st.expander("🔎 Advanced Filters", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        min_followers = st.slider(
            "Minimum Audience Size",
            min_value=1000,
            max_value=10000000,
            value=10000,
            step=1000,
            format="%d"
        )
        
    with col2:
        engagement_filter = st.slider(
            "Minimum Engagement Rate (%)",
            min_value=0.0,
            max_value=20.0,
            value=1.0,
            step=0.1,
            format="%.1f%%"
        )

# --- Niche Selection ---
st.subheader("✨ Select Your Niche")
st.markdown("Choose a category to find relevant influencers")

niches = df["Niche"].dropna().unique().tolist()
cols = st.columns(3)
for i, niche in enumerate(niches):
    with cols[i % 3]:
        if st.button(niche, key=f"niche_{i}", help=f"Show {niche} influencers"):
            st.session_state["selected_niche"] = niche

# --- Influencer Type Selection ---
if "selected_niche" in st.session_state:
    st.markdown("---")
    st.subheader(f"🎯 Select Influencer Tier for {st.session_state['selected_niche']}")
    st.caption("Choose based on audience size and influence level")
    
    influencer_types = df[df["Niche"] == st.session_state["selected_niche"]]["Influencer_Type"].unique()
    type_cols = st.columns(4)
    
    for i, infl_type in enumerate(influencer_types):
        with type_cols[i % 4]:
            if st.button(
                infl_type,
                key=f"type_{i}",
                help=f"Show {infl_type} influencers in {st.session_state['selected_niche']}"
            ):
                st.session_state["selected_category"] = infl_type
                st.switch_page("pages/3_list_page.py")

# --- Platform Stats ---
st.markdown("---")
st.subheader("📊 Platform Overview")
platform_cols = st.columns(2)

with platform_cols[0]:
    st.metric("Total Instagram Influencers", 
              value=f"{len(df[df['followers'].notna()]):,}",
              help="Creators with Instagram profiles")

with platform_cols[1]:
    st.metric("Total YouTube Creators", 
              value=f"{len(df[df['subscribers'].notna()]):,}",
              help="Creators with YouTube channels")

# --- How It Works ---
st.markdown("---")
st.subheader("💡 How It Works")
with st.expander("Learn how to find the perfect influencers"):
    st.markdown("""
    1. **Select a Niche** - Choose your industry or content category
    2. **Choose Influencer Tier** - Pick based on audience size
    3. **Refine Results** - Use filters to narrow down creators
    4. **Analyze Profiles** - View detailed analytics for each influencer
    5. **Create Campaigns** - Save favorites and build outreach lists
    
    Our platform combines data from both Instagram and YouTube to give you
    the most comprehensive influencer discovery experience.
    """)

# --- Empty State ---
if "selected_niche" not in st.session_state:
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(str(Path(__file__).parent / "assets/search_placeholder.png", width=300)
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <h4>Select a niche to begin your search</h4>
            <p>We'll show you the best influencers across both platforms</p>
        </div>
        """, unsafe_allow_html=True)
