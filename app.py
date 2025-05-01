import streamlit as st

st.set_page_config(page_title="Influencer Discovery", layout="wide")

# Updated CSS to fully style the sidebar
st.markdown("""
    <style>
    /* Sidebar container */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f1f5ff, #e3ecff);
        padding: 2rem 1rem;
        border-right: 1px solid #ddd;
    }

    /* Sidebar nav styling */
    [data-testid="stSidebarNav"] ul {
        padding: 0;
    }

    [data-testid="stSidebarNav"] li {
        list-style: none;
        margin-bottom: 1.2rem;
        font-size: 1.1rem;
        font-weight: 500;
    }

    [data-testid="stSidebarNav"] li a {
        text-decoration: none;
        color: #333;
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        display: block;
        transition: background-color 0.3s ease;
    }

    [data-testid="stSidebarNav"] li a:hover {
        background-color: #dce8ff;
        color: #1a4ed8;
    }

    /* Active tab styling */
    [data-testid="stSidebarNav"] li a[aria-current="page"] {
        background-color: #4a80f0;
        color: white !important;
    }

    /* Main content padding */
    .block-container {
        padding: 2rem 3rem;
    }

    /* CTA Button styling */
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

# Main image and title
st.image("assets/HOMEPAGE.jpg", use_container_width=True)

st.markdown("""
## Welcome to Influencer Discovery 🔍
Explore influencers by niche and category.

.
""")

# Start button
if st.button("🚀 Start Exploring"):
    st.switch_page("pages/2_search_page.py")

