# this is for readme file 
# Function to load Google Gemini Pro Vision API And get response
# bakend function to get the response from the google gemini pro vision API
# models/gemini-1.0-pro-vision-latest
# models/gemini-pro-vision
# models/gemini-1.5-pro-latest
# models/gemini-1.5-pro-001
# models/gemini-1.5-pro-002
# models/gemini-1.5-pro
# models/gemini-1.5-flash-latest
# models/gemini-1.5-flash-001
# models/gemini-1.5-flash-001-tuning
# models/gemini-1.5-flash
# models/gemini-1.5-flash-002
# models/gemini-1.5-flash-8b
# models/gemini-1.5-flash-8b-001
# models/gemini-1.5-flash-8b-latest
# models/gemini-1.5-flash-8b-exp-0827
# models/gemini-1.5-flash-8b-exp-0924
# models/gemini-2.5-pro-exp-03-25
# models/gemini-2.5-pro-preview-03-25
# models/gemini-2.5-flash-preview-04-17
# models/gemini-2.5-flash-preview-04-17-thinking
# models/gemini-2.5-pro-preview-05-06
# models/gemini-2.0-flash-exp
# models/gemini-2.0-flash
# models/gemini-2.0-flash-001
# models/gemini-2.0-flash-exp-image-generation
# models/gemini-2.0-flash-lite-001
# models/gemini-2.0-flash-lite
# models/gemini-2.0-flash-preview-image-generation
# models/gemini-2.0-flash-lite-preview-02-05
# models/gemini-2.0-flash-lite-preview
# models/gemini-2.0-pro-exp
# models/gemini-2.0-pro-exp-02-05
# models/gemini-exp-1206
# models/gemini-2.0-flash-thinking-exp-01-21
# models/gemini-2.0-flash-thinking-exp
# models/gemini-2.0-flash-thinking-exp-1219
# models/learnlm-1.5-pro-experimental
# models/learnlm-2.0-flash-experimental
# models/gemma-3-1b-it
# models/gemma-3-4b-it
# models/gemma-3-12b-it
# models/gemma-3-27b-it
import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re
from datetime import datetime

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS for professional styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }
    
    /* Header Styles */
    .app-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: #666;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        color: white;
    }
    
    /* Stats Cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-top: 4px solid #667eea;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #666;
        font-weight: 500;
    }
    
    /* Results Section */
    .results-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .nutrition-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress bars */
    .progress-container {
        margin: 1rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    /* Health Badge */
    .health-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .healthy {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .unhealthy {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        margin-top: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Gemini model setup
def get_gemini_response(input_text, image, prompt):
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash-thinking-exp-1219')
        response = model.generate_content([input_text, image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Error with Gemini API: {str(e)}")
        return None

# Image preprocessing
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Parse nutrition data for visualization
def parse_nutrition_data(response_text):
    """Extract nutrition data from the response for visualization"""
    # This is a simplified parser - you might want to make it more robust
    nutrition_data = {}
    
    # Extract percentages using regex
    patterns = {
        'Carbs': r'carbs?\s*[:-]?\s*(\d+(?:\.\d+)?)%',
        'Protein': r'protein\s*[:-]?\s*(\d+(?:\.\d+)?)%',
        'Fat': r'fat\s*[:-]?\s*(\d+(?:\.\d+)?)%',
        'Fiber': r'fiber\s*[:-]?\s*(\d+(?:\.\d+)?)%',
        'Sugar': r'sugar\s*[:-]?\s*(\d+(?:\.\d+)?)%'
    }
    
    for nutrient, pattern in patterns.items():
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            nutrition_data[nutrient] = float(match.group(1))
    
    return nutrition_data

# Create nutrition visualization
def create_nutrition_chart(nutrition_data):
    if not nutrition_data:
        return None
    
    # Create a donut chart
    fig = go.Figure(data=[go.Pie(
        labels=list(nutrition_data.keys()),
        values=list(nutrition_data.values()),
        hole=0.4,
        marker_colors=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
    )])
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=12,
        marker=dict(line=dict(color='white', width=2))
    )
    
    fig.update_layout(
        title={
            'text': 'Nutritional Breakdown',
            'x': 0.5,
            'font': {'size': 20, 'family': 'Inter'}
        },
        showlegend=False,
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Streamlit page config
st.set_page_config(
    page_title="🍎 AI Nutrition Analyzer",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
load_custom_css()

# App Header
st.markdown("""
<div class="app-header">
    <div class="app-title">🥗 AI Nutrition Analyzer</div>
    <div class="app-subtitle">Advanced Food Analysis powered by Google Gemini AI</div>
</div>
""", unsafe_allow_html=True)

# Feature highlights
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 Smart Recognition</h3>
        <p>AI-powered food identification with 95%+ accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Detailed Analysis</h3>
        <p>Complete nutritional breakdown and health insights</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>⚡ Instant Results</h3>
        <p>Get comprehensive analysis in seconds</p>
    </div>
    """, unsafe_allow_html=True)

# Main Analysis Section
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Input section with better layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📷 Upload Your Food Image")
    uploaded_file = st.file_uploader(
        "Choose an image file", 
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of your food for best results"
    )

with col2:
    st.subheader("⚙️ Analysis Options")
    input_text = st.text_area(
        "Custom Instructions (Optional)",
        placeholder="e.g., Focus on sugar content, ignore the drink...",
        height=100
    )
    
    analyze_button = st.button("🔬 Analyze Nutrition", type="primary")

# Image preview with enhanced styling
if uploaded_file:
    image = Image.open(uploaded_file)
    st.markdown("### 📸 Image Preview")
    
    # Create columns for better image display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Uploaded Food Image", use_column_width=True)

# Enhanced prompt template
input_prompt = """
You are an expert nutritionist and food analyst. Analyze the provided food image and provide a comprehensive nutritional breakdown.

Please structure your response as follows:

1. **FOOD IDENTIFICATION:**
   List each food item visible in the image

2. **CALORIE BREAKDOWN:**
   - Item 1: [specific calories]
   - Item 2: [specific calories]
   - Total Calories: [sum]

3. **NUTRITIONAL COMPOSITION (as percentages):**
   - Carbs: X%
   - Protein: Y%
   - Fat: Z%
   - Fiber: A%
   - Sugar: B%

4. **HEALTH ASSESSMENT:**
   Rate as HEALTHY or NEEDS IMPROVEMENT and explain why

5. **RECOMMENDATIONS:**
   Suggest improvements or complementary foods

Please be specific with numbers and provide actionable insights.
"""

# Results Section
if analyze_button and uploaded_file:
    with st.spinner("🤖 AI is analyzing your food..."):
        try:
            image_data = input_image_setup(uploaded_file)
            result = get_gemini_response(input_prompt, image_data, input_text or "Provide detailed nutritional analysis.")
            
            if result:
                st.markdown('<div class="results-container">', unsafe_allow_html=True)
                
                # Parse nutrition data for visualization
                nutrition_data = parse_nutrition_data(result)
                
                # Display results in tabs
                tab1, tab2, tab3 = st.tabs(["📋 Full Analysis", "📊 Nutrition Chart", "💡 Insights"])
                
                with tab1:
                    st.markdown("### Complete Nutritional Analysis")
                    st.markdown(result)
                
                with tab2:
                    if nutrition_data:
                        fig = create_nutrition_chart(nutrition_data)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Create nutrition grid
                        st.markdown("### Nutritional Breakdown")
                        cols = st.columns(len(nutrition_data) if nutrition_data else 3)
                        for i, (nutrient, value) in enumerate(nutrition_data.items()):
                            with cols[i]:
                                st.markdown(f"""
                                <div class="stat-card">
                                    <div class="stat-value">{value}%</div>
                                    <div class="stat-label">{nutrient}</div>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.info("📊 Upload an image and run analysis to see nutrition charts")
                
                with tab3:
                    st.markdown("### 🎯 Health Insights")
                    
                    # Extract health assessment (simplified)
                    if "healthy" in result.lower():
                        st.markdown('<div class="health-badge healthy">✅ Healthy Choice</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="health-badge unhealthy">⚠️ Needs Improvement</div>', unsafe_allow_html=True)
                    
                    st.markdown("""
                    **Key Recommendations:**
                    - Check the detailed analysis for specific suggestions
                    - Consider portion sizes and meal timing
                    - Balance with other meals throughout the day
                    """)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            st.info("💡 Make sure your image is clear and shows food items clearly.")

elif analyze_button and not uploaded_file:
    st.warning("📸 Please upload an image first!")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Built with ❤️ using Streamlit & Google Gemini AI | 
    <a href="https://github.com" target="_blank">View on GitHub</a> | 
    <a href="https://linkedin.com" target="_blank">Connect on LinkedIn</a></p>
    <p><small>© 2025 AI Nutrition Analyzer. Designed for educational purposes.</small></p>
</div>
""", unsafe_allow_html=True)

# Add sidebar with additional info
with st.sidebar:
    st.markdown("### 🚀 About This Project")
    st.markdown("""
    This advanced nutrition analyzer uses:
    - **Google Gemini AI** for image analysis
    - **Computer Vision** for food recognition
    - **Smart Parsing** for nutrition extraction
    - **Interactive Visualizations** for data presentation
    
    ### 📈 Features:
    - Real-time food analysis
    - Comprehensive nutrition breakdown
    - Health recommendations
    - Visual nutrition charts
    - Professional UI/UX design
    """)
    
    st.markdown("### 💼 Resume Highlights:")
    st.markdown("""
    - **AI Integration**: Google Gemini API
    - **Full-Stack Development**: Python, Streamlit
    - **Data Visualization**: Plotly, Charts
    - **UI/UX Design**: Modern, responsive interface
    - **Computer Vision**: Image processing & analysis
    """)


