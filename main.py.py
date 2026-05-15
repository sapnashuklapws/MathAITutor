import streamlit as st
from google import genai
from PIL import Image

# --- PAGE SETUP ---
st.set_page_config(page_title="Math AI Tutor", layout="centered")
st.title("🧠 Socratic Math Tutor")
st.write("Upload your math work, and I'll guide you through it!")

# --- API CONNECTION ---
try:
    # This reads the secret you added in Streamlit Settings
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("Error: API Key not found. Please check your Streamlit Secrets.")
    st.stop()

# --- APP LOGIC ---
uploaded_file = st.file_uploader("Upload a photo of your math work", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Your Solution", width='stretch')

    if st.button("Check My Solution"):
        with st.spinner("Analyzing your steps..."):
            try:
                # The Socratic Prompt instructions for the AI
                prompt_text = (
                    "You are a Socratic Math Tutor. Look at the image provided. "
                    "1. Check if the solution is correct. "
                    "2. If correct, congratulate the student. "
                    "3. If wrong, point out the FIRST mistake without giving the answer. "
                    "4. Provide a hint to help them think of the next step."
                )
                
                # Send to Gemini
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=[prompt_text, img]
                )
                
                # Show results
                st.subheader("📝 Tutor Feedback:")
                st.info(response.text)
                
            except Exception as ai_err:
                st.error(f"AI Error: {ai_err}")
