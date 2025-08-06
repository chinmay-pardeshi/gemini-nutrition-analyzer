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

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model setup
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('models/gemini-2.0-flash-thinking-exp-1219')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

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

# Streamlit page config
st.set_page_config(
    page_title="🍎 Gemini Health Analyzer",
    layout="centered",
)

# App Header
st.title("🥗 Gemini Health Nutrition Analyzer")
st.markdown("Upload a food image and get a detailed nutrition analysis powered by Gemini Pro Vision!")

# Input Fields
with st.form("calorie_form"):
    input_text = st.text_input("🔤 Custom Input (Optional)", placeholder="e.g., Estimate calories from this meal")
    uploaded_file = st.file_uploader("📷 Upload a Food Image", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("🍽️ Analyze Food & Calories")

# Image Preview
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Prompt Template
input_prompt = """
You are a nutrition expert. Based on the image provided, identify all food items and calculate total calories.
List each item with its respective calorie count as:

1. Item - Calories

Then analyze whether the meal is healthy or not.
Provide percentage split of carbs, protein, sugar, fat, fibers, and other dietary components.
Summarize total calories and mark healthy vs unhealthy components.
"""

# Output Section
if submitted:
    try:
        with st.spinner("🔍 Analyzing image and generating response..."):
            image_data = input_image_setup(uploaded_file)
            result = get_gemini_response(input_prompt, image_data, input_text or "Analyze this meal.")
            st.success("✅ Analysis Complete!")
            st.subheader("🧾 Nutritional Breakdown:")
            st.markdown(result)
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")




