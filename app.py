
import streamlit as st

# Page settings - updated with better defaults
st.set_page_config(
    page_title="Influencer Discovery",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🔍"
)

# Premium dark theme CSS with animations
st.markdown("""
    <style>
    /* Main content area */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Black sidebar with gradient accent */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000, #1a1a1a) !important;
        color: white !important;
        padding: 2.5rem 1.5rem !important;
        box-shadow: 5px 0 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar text styling */
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
        background: rgba(255,255,255,0.1);
        transform: translateX(5px);
    }
    
    /* Hero section */
    .hero {
        position: relative;
        margin-bottom: 3rem;
    }
    
    .hero-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(transparent, rgba(0,0,0,0.7));
        padding: 3rem;
        color: white;
    }
    
    /* Welcome text styling */
    .welcome-text h1 {
        font-size: 3.5rem;
        background: linear-gradient(90deg, #4A80F0, #8E2DE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 1.5rem;
        line-height: 1.2;
    }
    
    .welcome-text p {
        font-size: 1.4rem;
        color: #555;
        margin-bottom: 3rem;
        max-width: 800px;
    }
    
    /* Modern card styling */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #4A80F0;
    }
    
    /* Button style */
    .cta-button {
        background: linear-gradient(135deg, #4A80F0, #8E2DE2) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        font-size: 1.2rem !important;
        border-radius: 50px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(74, 128, 240, 0.3) !important;
        margin-top: 1rem !important;
    }
    
    .cta-button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(74, 128, 240, 0.4) !important;
    }
    
    /* Stats counter */
    .stats-container {
        background: linear-gradient(135deg, #4A80F0, #8E2DE2);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 3rem 0;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation - enhanced with icons
with st.sidebar:
    st.image("assets/HOMEPAGE.jpg", width=150)
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
            <li>📅 Recent Views</li>
            <li>📋 My Lists</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content - hero section
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div class="welcome-text">
        <h1>Discover Premium Influencers Across All Platforms</h1>
        <p>Unlock the power of data-driven influencer marketing with our comprehensive discovery platform. 
        Analyze millions of creators across Instagram, YouTube, and TikTok in seconds.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button with icon
    if st.button("🚀 Start Exploring Now", key="main_cta", use_container_width=True, type="primary"):
        st.switch_page("pages/2_search_page.py")

with col2:
    st.image("https://via.placeholder.com/500x400/f8f9fa/4A80F0?text=Platform+Integration", use_column_width=True)

# Stats counter
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

# Platform showcase
st.subheader("📱 Supported Platforms")
platform_cols = st.columns(3)
platforms = [
    {"name": "Instagram", "color": "#E1306C", "icon": "📸"},
    {"name": "YouTube", "color": "#FF0000", "icon": "▶️"},
    {"name": "TikTok", "color": "#000000", "icon": "🎵"}
]

for idx, platform in enumerate(platforms):
    with platform_cols[idx]:
        st.markdown(f"""
        <div style="background: {platform['color']}; color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">{platform['icon']}</div>
            <h3 style="color: white; margin-bottom: 0.5rem;">{platform['name']}</h3>
            <p style="opacity: 0.9;">Full analytics and discovery for {platform['name']} creators</p>
        </div>
        """, unsafe_allow_html=True)

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

