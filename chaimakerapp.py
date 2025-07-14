import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime
import time

st.set_page_config(
    page_title="रंग-ए-चाय - Chai Maker Pro",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize all session state variables with default values."""
    session_defaults = {
        "submitted": False,
        "recipes": [],
        "current_recipe": None,
        "show_form": True,
        "page_view": "create"
    }
    
    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

def load_custom_css():
    """Load all custom CSS styles for the application."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@300;400;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
        
        /* Global Styles */
        .main {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Background Video - Reduced brightness for better text contrast */
        #video-background {
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            z-index: -1;
            filter: brightness(0.1) blur(3px) contrast(0.8);
            object-fit: cover;
        }
        
        /* Content Overlay - Enhanced for better text visibility */
        .overlay-content {
            position: relative;
            z-index: 999;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 215, 0, 0.4);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        }
        
        /* Dark mode adjustments */
        @media (prefers-color-scheme: dark) {
            .overlay-content {
                background: rgba(40, 44, 52, 0.95);
                border: 2px solid rgba(255, 215, 0, 0.5);
                color: #e2e8f0;
            }
        }
        
        /* Header Styles - Enhanced contrast */
        .main-header {
            text-align: center;
            color: #FFD700 !important;
            font-family: 'Amiri', serif;
            font-size: 4rem;
            font-weight: 700;
            text-shadow: 3px 3px 8px rgba(0,0,0,0.9);
            margin-bottom: 5px;
            letter-spacing: 2px;
            background: rgba(0, 0, 0, 0.8);
            padding: 25px;
            border-radius: 15px;
            border: 2px solid #FFD700;
        }
        
        .sub-header {
            text-align: center;
            color: #FFF8DC !important;
            font-size: 1.3rem;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
            margin-bottom: 20px;
            background: rgba(0, 0, 0, 0.7);
            padding: 15px;
            border-radius: 10px;
        }
        
        /* Tagline Section - Better visibility */
        .tagline-section {
            text-align: center;
            margin: 25px 0;
            padding: 30px;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 15px;
            border: 3px solid #FFD700;
            box-shadow: 0 15px 50px rgba(255, 215, 0, 0.3);
            backdrop-filter: blur(15px);
        }
        
        @media (prefers-color-scheme: dark) {
            .tagline-section {
                background: rgba(40, 44, 52, 0.98);
                color: #e2e8f0;
            }
        }
        
        .hindi-tagline {
            font-family: 'Noto Sans Devanagari', sans-serif;
            font-size: 2.2rem;
            font-weight: 600;
            color: #8B4513 !important;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
            margin-bottom: 10px;
            line-height: 1.4;
        }
        
        @media (prefers-color-scheme: dark) {
            .hindi-tagline {
                color: #FFD700 !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }
        }
        
        .tagline-translation {
            font-family: 'Poppins', sans-serif;
            font-size: 1.2rem;
            font-weight: 400;
            color: #8B4513 !important;
            font-style: italic;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
            margin-top: 8px;
        }
        
        @media (prefers-color-scheme: dark) {
            .tagline-translation {
                color: #FFF8DC !important;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            }
        }
        
        /* Image Gallery - Enhanced background */
        .image-gallery {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
            margin: 30px 0;
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 215, 0, 0.3);
        }
        
        @media (prefers-color-scheme: dark) {
            .image-gallery {
                background: rgba(40, 44, 52, 0.95);
                border: 2px solid rgba(255, 215, 0, 0.4);
            }
        }
        
        .chai-image {
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 3px solid #FFD700;
        }
        
        .chai-image:hover {
            transform: scale(1.05);
            box-shadow: 0 12px 48px rgba(255,215,0,0.4);
        }
        
        /* Form Styles - Enhanced visibility */
        .stForm {
            background: rgba(255, 255, 255, 0.98) !important;
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
            margin: 25px 0;
            border: 3px solid #FFD700;
            backdrop-filter: blur(20px);
        }
        
        @media (prefers-color-scheme: dark) {
            .stForm {
                background: rgba(40, 44, 52, 0.98) !important;
                color: #e2e8f0;
                border: 3px solid #FFD700;
            }
        }
        
        /* Streamlit component styling - Enhanced contrast */
        .stSelectbox > div > div {
            background-color: rgba(255, 255, 255, 0.98) !important;
            border: 2px solid #8B4513 !important;
            border-radius: 8px !important;
            color: #2c3e50 !important;
            font-weight: 500 !important;
        }
        
        .stNumberInput > div > div {
            background-color: rgba(255, 255, 255, 0.98) !important;
            border: 2px solid #8B4513 !important;
            border-radius: 8px !important;
            color: #2c3e50 !important;
            font-weight: 500 !important;
        }
        
        .stTextInput > div > div {
            background-color: rgba(255, 255, 255, 0.98) !important;
            border: 2px solid #8B4513 !important;
            border-radius: 8px !important;
            color: #2c3e50 !important;
            font-weight: 500 !important;
        }
        
        .stTextArea > div > div {
            background-color: rgba(255, 255, 255, 0.98) !important;
            border: 2px solid #8B4513 !important;
            border-radius: 8px !important;
            color: #2c3e50 !important;
            font-weight: 500 !important;
        }
        
        .stMultiSelect > div > div {
            background-color: rgba(255, 255, 255, 0.98) !important;
            border: 2px solid #8B4513 !important;
            border-radius: 8px !important;
            color: #2c3e50 !important;
            font-weight: 500 !important;
        }
        
        .stSlider > div > div {
            background-color: rgba(255, 255, 255, 0.95) !important;
            border-radius: 8px !important;
            padding: 10px;
        }
        
        .stRadio > div {
            background-color: rgba(255, 255, 255, 0.95) !important;
            border-radius: 8px !important;
            padding: 10px;
            border: 1px solid #8B4513;
        }
        
        /* Dark mode adjustments for Streamlit components */
        @media (prefers-color-scheme: dark) {
            .stSelectbox > div > div,
            .stNumberInput > div > div,
            .stTextInput > div > div,
            .stTextArea > div > div,
            .stMultiSelect > div > div {
                background-color: rgba(45, 55, 72, 0.98) !important;
                border: 2px solid #FFD700 !important;
                color: #e2e8f0 !important;
            }
            
            .stSlider > div > div,
            .stRadio > div {
                background-color: rgba(45, 55, 72, 0.95) !important;
                border: 1px solid #FFD700;
            }
        }
        
        /* Enhanced text contrast for all elements */
        .stSelectbox label, .stNumberInput label, .stTextInput label, 
        .stTextArea label, .stMultiSelect label, .stSlider label,
        .stRadio label {
            color: #2c3e50 !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
            background: rgba(255, 255, 255, 0.9);
            padding: 5px 10px;
            border-radius: 5px;
            margin-bottom: 8px;
            display: inline-block;
        }
        
        @media (prefers-color-scheme: dark) {
            .stSelectbox label, .stNumberInput label, .stTextInput label,
            .stTextArea label, .stMultiSelect label, .stSlider label,
            .stRadio label {
                color: #e2e8f0 !important;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
                background: rgba(45, 55, 72, 0.9);
            }
        }
        
        /* Markdown text enhancement */
        .stMarkdown {
            color: #2c3e50 !important;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
            background: rgba(255, 255, 255, 0.9);
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #8B4513 !important;
            font-weight: 700 !important;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        }
        
        @media (prefers-color-scheme: dark) {
            .stMarkdown {
                color: #e2e8f0 !important;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
                background: rgba(45, 55, 72, 0.9);
            }
            
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                color: #FFD700 !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }
        }
        
        /* Button Styles - Enhanced */
        .stButton > button {
            background: linear-gradient(45deg, #8B4513, #D2691E) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 15px 30px !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 8px 25px rgba(139,69,19,0.4) !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
            border: 2px solid #FFD700 !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(45deg, #A0522D, #CD853F) !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 30px rgba(139,69,19,0.5) !important;
        }
        
        /* Success Message - Enhanced visibility */
        .success-message {
            background: linear-gradient(45deg, #32CD32, #228B22) !important;
            color: white !important;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-size: 20px;
            font-weight: 700;
            margin: 25px 0;
            box-shadow: 0 10px 30px rgba(50,205,50,0.4);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            border: 3px solid #90EE90;
        }
        
        /* Recipe Card - Enhanced visibility */
        .recipe-card {
            background: rgba(255, 248, 220, 0.98) !important;
            border-radius: 15px;
            padding: 30px;
            margin: 25px 0;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            border: 3px solid #8B4513;
            backdrop-filter: blur(15px);
        }
        
        @media (prefers-color-scheme: dark) {
            .recipe-card {
                background: rgba(45, 55, 72, 0.98) !important;
                color: #e2e8f0;
                border: 3px solid #FFD700;
            }
        }
        
        .recipe-title {
            color: #8B4513 !important;
            text-align: center;
            margin-bottom: 15px;
            font-size: 2rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        }
        
        @media (prefers-color-scheme: dark) {
            .recipe-title {
                color: #FFD700 !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }
        }
        
        .recipe-tagline {
            font-family: 'Noto Sans Devanagari', sans-serif;
            font-size: 1.2rem;
            color: #D2691E !important;
            text-align: center;
            font-style: italic;
            margin-bottom: 20px;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
            font-weight: 600;
        }
        
        @media (prefers-color-scheme: dark) {
            .recipe-tagline {
                color: #FFF8DC !important;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            }
        }
        
        /* Developer Section - Enhanced */
        .developer-section {
            background: linear-gradient(135deg, #2C3E50, #34495E) !important;
            color: white !important;
            padding: 35px;
            border-radius: 15px;
            margin: 35px 0;
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
            text-align: center;
            border: 3px solid #3498DB;
            backdrop-filter: blur(15px);
        }
        
        .developer-name {
            font-size: 2.2rem;
            font-weight: 700;
            color: #3498DB !important;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }
        
        .developer-title {
            font-size: 1.3rem;
            color: #BDC3C7 !important;
            margin-bottom: 20px;
            font-weight: 500;
        }
        
        .developer-description {
            font-size: 1.2rem;
            margin-bottom: 25px;
            color: #ECF0F1 !important;
            line-height: 1.6;
        }
        
        .linkedin-button {
            display: inline-block;
            background: linear-gradient(45deg, #0077B5, #005885) !important;
            color: white !important;
            padding: 15px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 700;
            font-size: 18px;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(0,119,181,0.4);
            margin: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            border: 2px solid rgba(255,255,255,0.3);
        }
        
        .linkedin-button:hover {
            background: linear-gradient(45deg, #005885, #0077B5) !important;
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0,119,181,0.5);
            text-decoration: none;
            color: white !important;
        }
        
        /* Footer with Tagline - Enhanced */
        .footer-tagline {
            font-family: 'Noto Sans Devanagari', sans-serif;
            font-size: 1.4rem;
            color: #FFD700 !important;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
            font-weight: 600;
        }
        
        /* Sidebar enhancement */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.98) !important;
            backdrop-filter: blur(15px);
            border-right: 3px solid #FFD700;
        }
        
        @media (prefers-color-scheme: dark) {
            .css-1d391kg {
                background: rgba(40, 44, 52, 0.98) !important;
                border-right: 3px solid #FFD700;
            }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2.8rem;
                padding: 20px;
            }
            .sub-header {
                font-size: 1.1rem;
                padding: 12px;
            }
            .hindi-tagline {
                font-size: 1.6rem;
            }
            .tagline-translation {
                font-size: 1rem;
            }
            .image-gallery {
                flex-direction: column;
                align-items: center;
                padding: 20px;
            }
            .developer-name {
                font-size: 1.8rem;
            }
            .stForm {
                padding: 25px;
            }
            .overlay-content {
                padding: 20px;
                margin: 10px 0;
            }
        }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

def render_background_video():
    """Render background video with enhanced overlay for better text visibility."""
    st.markdown("""
    <style>
        .background-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }
        
        #video-background {
            position: absolute;
            top: 50%;
            left: 50%;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            transform: translate(-50%, -50%);
            filter: brightness(0.08) blur(4px) contrast(0.7);
            object-fit: cover;
        }
        
        .background-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, 
                rgba(139, 69, 19, 0.95) 0%, 
                rgba(210, 105, 30, 0.95) 50%, 
                rgba(205, 133, 63, 0.95) 100%);
            background-size: 400% 400%;
            animation: gradientFlow 25s ease infinite;
        }
        
        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Additional overlay for maximum text contrast */
        .text-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.4);
        }
    </style>
    
    <div class="background-container">
        <div class="background-overlay"></div>
        <div class="text-overlay"></div>
        <video autoplay muted loop id="video-background" playsinline>
            <source src="https://cdn.pixabay.com/vimeo/336889682/chai-14357.mp4?width=1280&hash=119b3f3d144b99792abac8b83ab356f2636fa373" type="video/mp4">
            <source src="https://videos.pexels.com/video-files/2325178/2325178-hd_1920_1080_25fps.mp4" type="video/mp4">
            <source src="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4" type="video/mp4">
        </video>
    </div>
    """, unsafe_allow_html=True)

render_background_video()

st.markdown("""
<div class="main-header">
    रंग-ए-चाय ☕
</div>
<div class="sub-header">
    जहाँ हर चुस्की में कहानी हो | Where every sip tells a story
</div>
<div class="tagline-section">
    <div class="hindi-tagline">अपनी परफेक्ट चाय बनाएं</div>
    <div class="tagline-translation">Create Your Perfect Chai Experience</div>
</div>
""", unsafe_allow_html=True)

# IMAGE GALLERY 
@st.cache_data
def get_chai_images():
    """Get cached list of chai images with fallback URLs."""
    return [
        "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop",
        "https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=400&h=300&fit=crop",
        "https://images.unsplash.com/photo-1597318181409-cf64d0b3c200?w=400&h=300&fit=crop",
        "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=400&h=300&fit=crop",
        "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=300&fit=crop"
    ]

def create_image_gallery():
    """Create an interactive rotating image gallery."""
    image_urls = get_chai_images()
    
    gallery_html = f"""
    <div class="image-gallery">
        <img id="img1" src="{image_urls[0]}" width="300" height="200" class="chai-image" 
             onerror="this.src='https://via.placeholder.com/300x200/8B4513/FFFFFF?text=Chai+Image'" 
             loading="lazy" alt="Chai Image 1">
        <img id="img2" src="{image_urls[1]}" width="300" height="200" class="chai-image" 
             onerror="this.src='https://via.placeholder.com/300x200/8B4513/FFFFFF?text=Chai+Image'" 
             loading="lazy" alt="Chai Image 2">
        <img id="img3" src="{image_urls[2]}" width="300" height="200" class="chai-image" 
             onerror="this.src='https://via.placeholder.com/300x200/8B4513/FFFFFF?text=Chai+Image'" 
             loading="lazy" alt="Chai Image 3">
    </div>

    <script>
    (function() {{
        const images = {json.dumps(image_urls)};
        let currentIndex = 3;
        
        function rotateImages() {{
            const img1 = document.getElementById("img1");
            const img2 = document.getElementById("img2");
            const img3 = document.getElementById("img3");
            
            if (img1 && img2 && img3) {{
                [img1, img2, img3].forEach(img => img.style.opacity = "0.7");
                
                setTimeout(() => {{
                    img1.src = images[currentIndex % images.length];
                    img2.src = images[(currentIndex + 1) % images.length];
                    img3.src = images[(currentIndex + 2) % images.length];
                    
                    [img1, img2, img3].forEach(img => img.style.opacity = "1");
                    
                    currentIndex = (currentIndex + 1) % images.length;
                }}, 300);
            }}
        }}
        
        setTimeout(() => {{
            setInterval(rotateImages, 4000);
        }}, 1000);
    }})();
    </script>
    """
    
    return gallery_html

components.html(create_image_gallery(), height=280)

def render_sidebar():
    """Render sidebar with helpful information."""
    with st.sidebar:
        st.markdown("### Chai Benefits")
        st.markdown("""
        - **Antioxidants**: Rich in polyphenols that fight free radicals
        - **Digestion**: Ginger and cardamom aid digestive health
        - **Immunity**: Spices naturally boost immune system
        - **Energy**: Provides sustained natural caffeine boost
        - **Warmth**: Perfect comfort drink for any weather
        """)
        
        st.markdown("### Popular Combinations")
        st.markdown("""
        - **Classic Masala**: Black tea + Milk + Ginger + Cardamom
        - **Strong Spiced**: Strong + All spices + Whole milk
        - **Green Tea**: Green tea + Honey + Fresh mint
        - **Pure Herbal**: Herbal tea + Tulsi + No milk
        - **Royal Saffron**: Black tea + Milk + Saffron + Cardamom
        """)
        
        st.markdown("### Perfect Chai Tips")
        st.markdown("""
        - Use fresh, whole spices for best flavor
        - Boil water first, then add tea
        - Add milk gradually to prevent curdling
        - Strain well before serving
        - Adjust sweetness to personal preference
        """)

render_sidebar()

def render_navigation():
    """Render top navigation buttons."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Create New Recipe", key="nav_create", use_container_width=True):
            st.session_state.page_view = "create"
            st.session_state.show_form = True
            st.session_state.submitted = False
            st.session_state.current_recipe = None
    
    with col2:
        if st.button("View Current Recipe", key="nav_view", use_container_width=True, 
                    disabled=not st.session_state.current_recipe):
            st.session_state.page_view = "view"
            st.session_state.show_form = False
            st.session_state.submitted = True
    
    with col3:
        if st.button("Recipe History", key="nav_history", use_container_width=True):
            st.session_state.page_view = "history"
            st.session_state.show_form = False
            st.session_state.submitted = False

render_navigation()

def generate_chai_name(mood, spices, addons, strength, tea_type, milk_type, sweetness):
    """Generate a creative chai name based on user selections."""
    mood_words = {
        "Energetic": "Energetic", "Relaxed": "Calm", "Focused": "Sharp",
        "Cozy": "Cozy", "Adventurous": "Bold"
    }
    
    name_parts = [mood_words.get(mood, "Classic")]
    
    if "Fresh Ginger" in spices:
        name_parts.append("Ginger")
    if "Green Cardamom" in spices:
        name_parts.append("Cardamom")
    if "Holy Basil (Tulsi)" in addons:
        name_parts.append("Tulsi")
    if strength == "Strong":
        name_parts.append("Strong")
    if "Green Tea" in tea_type:
        name_parts.append("Green")
    if milk_type == "No Milk":
        name_parts.append("Black")
    if "Saffron" in addons:
        name_parts.append("Saffron")
    if sweetness >= 8:
        name_parts.append("Sweet")
    
    return " ".join(name_parts[:3] + ["Chai"])

def create_recipe_data(form_data):
    """Create structured recipe data from form inputs."""
    return {
        "name": form_data.get("name", "Anonymous"),
        "chai_name": generate_chai_name(
            form_data["mood"], form_data["spices"], form_data["addons"],
            form_data["strength"], form_data["tea_type"], form_data["milk_type"],
            form_data["sweetness"]
        ),
        "mood": form_data["mood"],
        "tea_type": form_data["tea_type"],
        "milk_type": form_data["milk_type"],
        "sweetness": form_data["sweetness"],
        "strength": form_data["strength"],
        "boil_time": form_data["boil_time"],
        "temperature": form_data["temperature"],
        "spices": form_data["spices"],
        "addons": form_data["addons"],
        "uploaded_image": form_data.get("uploaded_image"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def render_chai_form():
    """Render the main chai customization form."""
    with st.form("chai_form"):
        st.markdown("## Customize Your Perfect Chai")
        
        col_name, col_mood = st.columns(2)
        with col_name:
            name = st.text_input(
                "Your Name", 
                placeholder="e.g., Naman", 
                help="Tell us your name for a personalized experience"
            )
        with col_mood:
            mood = st.selectbox(
                "Current Mood", 
                ["Energetic", "Relaxed", "Focused", "Cozy", "Adventurous"],
                help="Your mood influences the chai name generation"
            )

        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Tea Base Configuration**")
            tea_type = st.selectbox(
                "Tea Type", 
                ["Black Tea", "Green Tea", "Herbal Tea", "White Tea", "Oolong Tea"]
            )
            strength = st.radio(
                "Tea Strength", 
                ["Light", "Medium", "Strong"], 
                horizontal=True,
                help="Affects steeping time and flavor intensity"
            )
            
        with col2:
            st.markdown("**Milk & Sweetness**")
            milk_type = st.selectbox(
                "Milk Preference", 
                ["Whole Milk", "Skim Milk", "Almond Milk", "Oat Milk", 
                 "Coconut Milk", "Soy Milk", "No Milk"]
            )
            sweetness = st.slider(
                "Sweetness Level", 
                0, 10, 5, 
                help="0 = No sweetener, 10 = Very sweet"
            )
            
        with col3:
            st.markdown("**Preparation Settings**")
            boil_time = st.slider(
                "Boil Time (minutes)", 
                1, 15, 5,
                help="Longer boiling extracts more flavor"
            )
            temperature = st.selectbox(
                "Water Temperature", 
                ["Boiling (100°C)", "Hot (80-90°C)", "Warm (70-80°C)"]
            )

        st.markdown("---")
        
        col_spices, col_addons = st.columns(2)
        
        with col_spices:
            st.markdown("**Aromatic Spices**")
            spices = st.multiselect(
                "Choose Your Spices",
                ["Fresh Ginger", "Green Cardamom", "Cinnamon Stick", "Whole Cloves", 
                 "Black Pepper", "Star Anise", "Fennel Seeds", "Nutmeg"],
                help="Select multiple spices for complex flavor profiles"
            )
            
        with col_addons:
            st.markdown("**Premium Add-ons**")
            addons = st.multiselect(
                "Special Enhancements",
                ["Raw Honey", "Fresh Lemon", "Holy Basil (Tulsi)", "Fresh Mint", 
                 "Rose Petals", "Saffron", "Vanilla Extract", "Coconut Oil"]
            )

        st.markdown("---")
        
        st.markdown("**Share Your Chai Moment**")
        uploaded_image = st.file_uploader(
            "Upload a photo of your chai setup or finished cup",
            type=["jpg", "jpeg", "png", "webp"],
            help="Optional: Share your chai creation with the community"
        )
        
        submit = st.form_submit_button(
            "Create My Perfect Chai Recipe", 
            use_container_width=True
        )

        if submit:
            form_data = {
                "name": name,
                "mood": mood,
                "tea_type": tea_type,
                "milk_type": milk_type,
                "sweetness": sweetness,
                "strength": strength,
                "boil_time": boil_time,
                "temperature": temperature,
                "spices": spices,
                "addons": addons,
                "uploaded_image": uploaded_image
            }
            
            recipe_data = create_recipe_data(form_data)
            st.session_state.current_recipe = recipe_data
            st.session_state.recipes.append(recipe_data)
            st.session_state.submitted = True
            st.session_state.show_form = False
            st.session_state.page_view = "view"
            
            st.rerun()

def render_recipe_display(recipe_data):
    """Render the complete recipe display with all details."""
    with st.spinner("Preparing your perfect chai recipe..."):
        time.sleep(1)
    
    st.markdown(f"""
    <div class="success-message">
        Perfect chai recipe ready for {recipe_data['name']}!<br>
        Your {recipe_data['mood'].lower()} chai is ready to brew!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="recipe-card">
        <h2 class="recipe-title">Your Signature Chai: "{recipe_data['chai_name']}"</h2>
        <p class="recipe-tagline">जहाँ हर चुस्की में कहानी हो</p>
    </div>
    """, unsafe_allow_html=True)
    
    if recipe_data.get('uploaded_image'):
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.image(recipe_data['uploaded_image'], caption="Your Chai Creation", use_column_width=True)
    
    col_recipe1, col_recipe2 = st.columns(2)
    
    with col_recipe1:
        st.markdown("### Recipe Details")
        st.markdown(f"""
        **Creator:** {recipe_data['name']}  
        **Mood:** {recipe_data['mood']}  
        **Tea Base:** {recipe_data['tea_type']}  
        **Strength:** {recipe_data['strength']}  
        **Milk:** {recipe_data['milk_type']}  
        **Sweetness:** {recipe_data['sweetness']}/10  
        """)
        
    with col_recipe2:
        st.markdown("### Preparation Details")
        st.markdown(f"""
        **Boil Time:** {recipe_data['boil_time']} minutes  
        **Temperature:** {recipe_data['temperature']}  
        **Spices:** {', '.join(recipe_data['spices']) if recipe_data['spices'] else 'None'}  
        **Add-ons:** {', '.join(recipe_data['addons']) if recipe_data['addons'] else 'None'}  
        **Created:** {recipe_data['created_at']}  
        """)
    
    render_brewing_instructions(recipe_data)
    render_download_section(recipe_data)
    render_rating_section()
    render_recipe_management()

def render_brewing_instructions(recipe_data):
    """Render detailed step-by-step brewing instructions."""
    st.markdown("### Step-by-Step Brewing Instructions")
    
    instructions = f"""
    1. **Prepare Water**: Heat water to {recipe_data['temperature'].lower()}
    2. **Add Tea**: Add {recipe_data['tea_type'].lower()} leaves or bag to the water
    3. **Add Spices**: For aroma, add {', '.join(recipe_data['spices']) if recipe_data['spices'] else 'no spices'}
    4. **Boil**: Simmer for {recipe_data['boil_time']} minutes on {recipe_data['strength'].lower()} heat
    5. **Add Milk**: Pour in {recipe_data['milk_type'].lower()} and bring to a gentle boil
    6. **Add Sweetness**: Add sugar for {recipe_data['sweetness']}/10 sweetness level
    7. **Final Touch**: Before serving, add {', '.join(recipe_data['addons']) if recipe_data['addons'] else 'no special ingredients'}
    8. **Strain & Serve**: Strain through fine mesh and pour into your favorite cup
    """
    
    st.markdown(instructions)

def render_download_section(recipe_data):
    """Render download buttons for recipe export."""
    recipe_text = f"""
Rang-e-Chai - Tea Recipe
========================

Recipe Name: {recipe_data['chai_name']}
Creator: {recipe_data['name']}
Mood: {recipe_data['mood']}
Created: {recipe_data['created_at']}

Ingredients:
- Tea: {recipe_data['tea_type']} ({recipe_data['strength']} strength)
- Milk: {recipe_data['milk_type']}
- Sweetness: {recipe_data['sweetness']}/10
- Spices: {', '.join(recipe_data['spices']) if recipe_data['spices'] else 'None'}
- Add-ons: {', '.join(recipe_data['addons']) if recipe_data['addons'] else 'None'}

Preparation:
- Boil Time: {recipe_data['boil_time']} minutes
- Temperature: {recipe_data['temperature']}

Instructions:
1. Prepare Water: Heat water to {recipe_data['temperature'].lower()}
2. Add Tea: Add {recipe_data['tea_type'].lower()} leaves or bag to the water
3. Add Spices: For aroma, add {', '.join(recipe_data['spices']) if recipe_data['spices'] else 'no spices'}
4. Boil: Simmer for {recipe_data['boil_time']} minutes on {recipe_data['strength'].lower()} heat
5. Add Milk: Pour in {recipe_data['milk_type'].lower()} and bring to a gentle boil
6. Add Sweetness: Add sugar for {recipe_data['sweetness']}/10 sweetness level
7. Final Touch: Before serving, add {', '.join(recipe_data['addons']) if recipe_data['addons'] else 'no special ingredients'}
8. Strain & Serve: Strain through fine mesh and pour into your favorite cup

========================
Generated by Rang-e-Chai
Where every sip tells a story
Developed by: Naman Agrawal
LinkedIn: https://www.linkedin.com/in/naman-agrawal-8671aa27b/
"""
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            "Download Recipe (TXT)",
            recipe_text,
            file_name=f"{recipe_data['chai_name'].replace(' ', '_')}_recipe.txt",
            mime="text/plain",
            key="download_txt"
        )
    
    with col_dl2:
        json_data = {k: v for k, v in recipe_data.items() if k != 'uploaded_image'}
        st.download_button(
            "Download Recipe (JSON)",
            json.dumps(json_data, indent=2, ensure_ascii=False),
            file_name=f"{recipe_data['chai_name'].replace(' ', '_')}_recipe.json",
            mime="application/json",
            key="download_json"
        )

def render_rating_section():
    """Render rating and feedback section."""
    st.markdown("### Rate Your Experience")
    
    col_rating, col_feedback = st.columns(2)
    
    with col_rating:
        rating = st.slider(
            "How satisfied are you with this recipe?", 
            1, 5, 4, 
            key="rating_slider"
        )
        st.markdown(f"**Rating:** {'⭐' * rating} ({rating}/5)")
    
    with col_feedback:
        feedback = st.text_area(
            "Share your thoughts or suggestions:",
            placeholder="This recipe looks amazing! Can't wait to try it...",
            key="feedback_text"
        )
        if feedback:
            st.success("Thank you for your feedback!")

def render_recipe_management():
    """Render recipe management section."""
    st.markdown("### Recipe Management")
    
    uploaded_recipe = st.file_uploader(
        "Load saved recipe file", 
        type=["txt", "json"], 
        key="upload_recipe"
    )
    
    if uploaded_recipe:
        try:
            content = uploaded_recipe.read().decode("utf-8")
            st.code(content, language="text")
        except Exception as e:
            st.error(f"Error reading file: {e}")

def render_recipe_history():
    """Render the recipe history page."""
    st.markdown("## Recipe History")
    
    if st.session_state.recipes:
        for i, recipe in enumerate(reversed(st.session_state.recipes), 1):
            with st.expander(f"{i}. {recipe['chai_name']} - {recipe['created_at']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Creator:** {recipe['name']}  
                    **Mood:** {recipe['mood']}  
                    **Tea:** {recipe['tea_type']} ({recipe['strength']})  
                    **Milk:** {recipe['milk_type']}  
                    **Sweetness:** {recipe['sweetness']}/10  
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Boil Time:** {recipe['boil_time']} minutes  
                    **Temperature:** {recipe['temperature']}  
                    **Spices:** {', '.join(recipe['spices']) if recipe['spices'] else 'None'}  
                    **Add-ons:** {', '.join(recipe['addons']) if recipe['addons'] else 'None'}  
                    """)
                
                if st.button(f"Load Recipe {i}", key=f"load_{i}"):
                    st.session_state.current_recipe = recipe
                    st.session_state.submitted = True
                    st.session_state.show_form = False
                    st.session_state.page_view = "view"
                    st.rerun()
    else:
        st.info("No recipes created yet. Start by creating your first recipe!")

def render_developer_section():
    """Render the developer section with information and links."""
    st.markdown("""
    <div class="developer-section">
        <h2 class="developer-name">Naman Agrawal</h2>
        <p class="developer-title">Chai Enthusiast</p>
        <p class="developer-description">
            Passionate about crafting delightful user experiences and perfecting the art of chai making.
            This app is a tribute to my love for chai and technology.
        </p>
        <a href="https://www.linkedin.com/in/naman-agrawal-8671aa27b/" 
           class="linkedin-button" target="_blank">Connect on LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render the application footer with tagline."""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: white; padding: 20px; background: rgba(0,0,0,0.7); border-radius: 10px; margin-top: 30px;">
        <p class="footer-tagline">जहाँ हर चुस्की में कहानी हो</p>
        <p><strong>रंग-ए-चाय</strong> - Crafting perfect chai experiences since 2024</p>
        <p>Made with care for chai lovers worldwide | Developed by <strong>Naman Agrawal</strong></p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application logic with proper state management."""
    
    if st.session_state.page_view == "create" and st.session_state.show_form and not st.session_state.submitted:
        render_chai_form()
    
    elif st.session_state.page_view == "view" and st.session_state.submitted and st.session_state.current_recipe:
        render_recipe_display(st.session_state.current_recipe)
    
    elif st.session_state.page_view == "history":
        render_recipe_history()
    
    render_developer_section()
    render_footer()

if __name__ == "__main__":
    main()
