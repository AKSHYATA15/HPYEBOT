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
