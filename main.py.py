import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- Page Configuration ---
st.set_page_config(page_title="AI Math Tutor", page_icon="🔢")

st.title("🔢 Handwritten Math Checker")
st.markdown("Upload a photo of a math problem to verify the solution.")

# --- API Key Management ---
# 1. Check if the key is in Streamlit Secrets (for Cloud deployment)
# 2. Otherwise, check for user input in the sidebar
api_key = st.secrets.get("GEMINI_API_KEY")

with st.sidebar:
    st.header("Settings")
    if not api_key:
        api_key = st.text_input("Enter your Gemini API Key:", type="password")
        st.info("Get a key at [Google AI Studio](https://aistudio.google.com/)")
    else:
        st.success("API Key loaded from Cloud Secrets!")

# --- App Logic ---
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    if st.button("Analyze Math"):
        if not api_key:
            st.error("Missing API Key. Please provide it in the sidebar or Cloud Secrets.")
        else:
            try:
                genai.configure(api_key=api_key)
                #model = genai.GenerativeModel('gemini-1.5-flash')
                #model = genai.GenerativeModel('gemini-1.5-flash-latest')
                # Instead of 'gemini-1.5-flash'
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                with st.spinner('AI is checking the math...'):
                    prompt = "Identify the math problem in this image. Check if it is solved correctly. If there is a mistake, explain why and provide the correct step-by-step solution using LaTeX formatting."
                    response = model.generate_content([prompt, image])
                    
                    st.subheader("Analysis Result:")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

