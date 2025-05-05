import streamlit as st

# Page settings
st.set_page_config(
    page_title="Influencer Discovery",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🔍"
)

# CSS (excluding dark sidebar)
st.markdown(""" 
<style>
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
.welcome-text {
    text-align: center;
    max-width: 900px;
    margin: 0 auto 3rem auto;
}
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
}
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

.feature-container {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: #4A80F0;
}
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
.platform-card {
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s ease;
    margin-bottom: 1rem;
    cursor: pointer;
    border: 1px solid rgba(0,0,0,0.1);
}
.platform-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}
.platform-card img {
    width: 100%;
    height: auto;
    display: block;
}
.platform-button {
    width: 100%;
    border: none;
    background: linear-gradient(135deg, #4A80F0, #8E2DE2);
    color: white;
    padding: 0.75rem;
    font-weight: 600;
    border-radius: 0 0 12px 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}
.section-title {
    text-align: center;
    margin: 4rem 0 2rem 0;
    font-size: 2.5rem;
    background: linear-gradient(90deg, #4A80F0, #8E2DE2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}
@media (max-width: 768px) {
    .welcome-text h1 {
        font-size: 2.5rem;
    }
    .welcome-text p {
        font-size: 1.1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Hero Image
st.image("assets/HOMEPAGE.jpg", use_container_width=True)

# Welcome Section
st.markdown("""
<div class="welcome-text">
    <h1>Discover Premium Influencers Across All Platforms</h1>
    <p>Unlock the power of data-driven influencer marketing with our comprehensive discovery platform. 
    Analyze millions of creators across Instagram, YouTube, TikTok and more.</p>
</div>
""", unsafe_allow_html=True)




# Feature cards
st.subheader("✨ Key Features")
cols = st.columns(3)
with cols[0]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-container">
        <div class="feature-icon">🔍</div>
        <h3>Advanced Search</h3>
        <p>Filter by platform, niche, engagement rate, audience demographics,more with our powerful search engine.</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-container">
        <div class="feature-icon">📊</div>
        <h3>Deep Analytics</h3>
        <p>Get comprehensive performance metrics, audience insights, and content analysis for every influencer.</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-container">
        <div class="feature-icon">🤖</div>
        <h3>AI Recommendations</h3>
        <p>Our algorithm learns your preferences to suggest perfect influencer matches for your campaigns.</p>
    </div>
    </div>
    """, unsafe_allow_html=True)

# New Platform Explorer Section
st.markdown('<h1 class="section-title">Start Exploring</h1>', unsafe_allow_html=True)

# Platform cards with clickable images
platform_cols = st.columns(3)
platforms = [
    {"name": "Instagram", "image": "assets/Instagram.jpg", "page": "pages/2_search_page.py"},
    {"name": "YouTube", "image": "assets/youtube.jpg", "page": "pages/2_search_page.py"},
    {"name": "TikTok", "image": "assets/tiktok.jpg", "page": "pages/tiktok_platform.py"}
]

platform_cols = st.columns(3)
for idx, platform in enumerate(platforms):
    with platform_cols[idx]:
        st.image(platform["image"],width=200)
        if st.button(f"Explore {platform['name']} →", key=f"btn_{platform['name']}"):
            st.switch_page(platform["page"])

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
