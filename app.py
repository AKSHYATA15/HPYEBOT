import streamlit as st

# Page settings
st.set_page_config(page_title="Influencer Discovery", layout="wide")

# Custom CSS for modern aesthetic
st.markdown("""
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f9f9f9, #e0eaff);
        color: #000;
        padding: 2rem 1rem;
    }
    [data-testid="stSidebarNav"] > ul {
        font-size: 1.1rem;
    }
    [data-testid="stSidebarNav"] ul li {
        margin-bottom: 15px;
        font-weight: 500;
    }
    /* Center the content */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    /* Welcome text styling */
    .welcome-text h1 {
        font-size: 3rem;
        color: #31333F;
        font-weight: 800;
        margin-top: 2rem;
    }
    .welcome-text p {
        font-size: 1.3rem;
        color: #666;
        margin-bottom: 2rem;
    }
    /* Button style */
    div.stButton > button {
        background-color: #4A80F0;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        border-radius: 8px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #315fd1;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Display image
st.image("assets/HOMEPAGE.jpg", use_container_width=True)

# Text + button
st.markdown("""
<div class="welcome-text">
    <h1>Welcome to Influencer Discovery 🔍</h1>
    <p>Explore Instagram and YouTube influencers by niche and category.<br>
    Use the menu on the left to begin your journey.</p>
</div>
""", unsafe_allow_html=True)

# CTA Button
if st.button("🚀 Start Exploring"):
    st.switch_page("pages/2_search_page.py")
