import streamlit as st
from google import genai  # Use the new library
from PIL import Image

# Setup the Page Layout
st.set_page_config(page_title="Math Tutor AI", layout="centered")
st.title("🧠 Socratic Math Tutor")

# Connect to the AI using the new SDK
# Ensure your secret name in Streamlit matches "GEMINI_API_KEY"
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ... (rest of your file uploader code)

if uploaded_file:
    img = Image.open(uploaded_file)
    # Note: 'use_container_width' is deprecated in 2026; use width='stretch'
    st.image(img, caption="Your Work", width='stretch') 

    if st.button("Check My Solution"):
        with st.spinner("Analyzing..."):
            prompt = "You are a Socratic Math Tutor. [Your full prompt here]"
            
            # Use the updated method call for the new library
            response = client.models.generate_content(
                model="gemini-2.0-flash", # Use a current 2026 model name
                contents=[prompt, img]
            )
            
            st.markdown("### 📝 Tutor Feedback:")
            st.info(response.text)
