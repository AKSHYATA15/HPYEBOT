import streamlit as st
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="Influencer Discovery",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🔍"
)

# Get the absolute path to the assets folder
assets_path = Path(__file__).parent / "assets"

# Premium dark theme CSS with animations
st.markdown("""
    <style>
    /* [Previous CSS styles remain exactly the same] */
    .platform-logo {
        height: 100px;
        margin: 0 auto;
        display: block;
        padding: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image(str(assets_path / "Instagram logo.png"), width=150)
    st.markdown("""
    <div style="margin-top: 2rem; margin-bottom: 3rem;">
        <h3 style="color: white; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">🔍 Navigation</h3>
        <ul style="list-style: none; padding-left: 0;">
            <li>🏠 Home</li>
            <li>🔎 Search Influencers</li>
            <li>📊 Analytics Dashboard</li>
            <li>💌 Campaign Manager</li>
            <li>⚙️ Settings</li>
        </ul>
    </div>
    <div style="margin-top: 3rem;">
        <h3 style="color: white; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">📌 Quick Actions</h3>
        <ul style="list-style: none; padding-left: 0;">
            <li>⭐ Saved Searches</li>
            <li>🗕️ Recent Views</li>
            <li>📋 My Lists</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Hero Image - full-width first section
st.image(str(assets_path / "HOMEPAGE.jpg"), use_column_width=True)

# Welcome section - Centered
st.markdown("""
<div class="welcome-text">
    <h1>Discover Premium Influencers Across All Platforms</h1>
    <p>Unlock the power of data-driven influencer marketing with our comprehensive discovery platform. 
    Analyze millions of creators across Instagram, YouTube, and TikTok in seconds.</p>
</div>
""", unsafe_allow_html=True)

if st.button("🚀 Start Exploring Now", key="main_cta", use_container_width=True, type="primary"):
    st.switch_page("pages/2_search_page.py")

# Stats section
st.markdown("""
<div class="stats-container">
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
        <div class="stat-item">
            <div class="stat-number">250K+</div>
            <div class="stat-label">Influencers</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">50+</div>
            <div class="stat-label">Niches</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">10M+</div>
            <div class="stat-label">Data Points</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">95%</div>
            <div class="stat-label">Accuracy</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature cards
st.subheader("✨ Key Features")
cols = st.columns(3)
with cols[0]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <h3>Advanced Search</h3>
        <p>Filter by platform, niche, engagement rate, audience demographics, and more with our powerful search engine.</p>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Deep Analytics</h3>
        <p>Get comprehensive performance metrics, audience insights, and content analysis for every influencer.</p>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3>AI Recommendations</h3>
        <p>Our algorithm learns your preferences to suggest perfect influencer matches for your campaigns.</p>
    </div>
    """, unsafe_allow_html=True)

# New Platform Explorer Section
st.markdown('<h1 class="section-title">Start Exploring</h1>', unsafe_allow_html=True)

# Platform cards with logos
platform_cols = st.columns(3)
platforms = [
    {"name": "Instagram", "logo": "Instagram logo.png", "page": "pages/instagram.py"},
    {"name": "YouTube", "logo": "youtube logo.png", "page": "pages/youtube.py"},
    {"name": "TikTok", "logo": "tiktok logo.png", "page": "pages/tiktok.py"}
]

for idx, platform in enumerate(platforms):
    with platform_cols[idx]:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <img src="{str(assets_path / platform['logo'])}" class="platform-logo" alt="{platform['name']}">
            <h3>{platform['name']}</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Explore {platform['name']} →", key=f"btn_{platform['name']}", use_container_width=True):
            st.switch_page(platform['page'])

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666;">
    <p>© 2023 InfluenceX | Premium Influencer Discovery Platform</p>
    <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
        <span>Terms</span> | <span>Privacy</span> | <span>Contact</span>
    </div>
</div>
""", unsafe_allow_html=True)
