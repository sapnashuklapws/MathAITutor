import streamlit as st
from google import genai  # Correct new library
from PIL import Image

# 1. Setup the Page Layout
st.set_page_config(page_title="Math Tutor AI", layout="centered")
st.title("🧠 Socratic Math Tutor")

# 2. Connect to the AI
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Create the Uploader (THIS MUST COME FIRST)
# This line creates the variable 'uploaded_file'
uploaded_file = st.file_uploader("Upload your math work", type=["jpg", "png", "jpeg"])

# 4. Now you can check if the file exists
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Your Work", width='stretch')

    if st.button("Check My Solution"):
        with st.spinner("Analyzing..."):
            prompt = "You are a Socratic Math Tutor..."
            
            # Use the correct method for the new library
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=[prompt, img]
            )
            
            st.markdown("### 📝 Tutor Feedback:")
            st.info(response.text)
