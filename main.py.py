import streamlit as st
from google import genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="AI Math Tutor", layout="centered")
st.title("🧠 Socratic Math Tutor")

# 2. Secure API Connection
try:
    # This pulls your key from the Streamlit "Secrets" setting
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# 3. File Uploader
uploaded_file = st.file_uploader("Upload a photo of your math work", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Your Work", width='stretch')

    if st.button("Check My Solution"):
        with st.spinner("Talking to the AI Tutor..."):
            try:
                # The Socratic Prompt
                prompt = """
                Analyze this image. It has a math problem and a student's solution.
                - If correct, say 'Good work!'.
                - If wrong, find the FIRST mistake and give a Socratic hint.
                - DO NOT give the final answer.
                """
                
                # We use 'gemini-1.5-flash' as it is the most stable free model
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=[prompt, img]
                )
                
                st.subheader("📝 Tutor Feedback:")
                st.info(response.text)
                
            except Exception as ai_err:
                st.error(f"AI Error: {ai_err}")
                st.write("Tip: Double-check if the model name is correct or if your API key has expired.")
