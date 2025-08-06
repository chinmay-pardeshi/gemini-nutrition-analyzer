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
