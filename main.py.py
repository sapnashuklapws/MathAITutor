import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup the Page Layout
st.set_page_config(page_title="Math Tutor AI", layout="centered")
st.title("🧠 Socratic Math Tutor")
st.write("Upload your math work, and I'll help you find your mistakes!")

# 2. Connect to the AI (Replace with your actual key for testing)
# Note: For the Cloud version, we will use a safer method!
API_KEY = "YOUR_PASTE_KEY_HERE" 
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Create the Image Uploader
uploaded_file = st.file_uploader("Upload a photo of your math problem", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Open and show the image
    img = Image.open(uploaded_file)
    st.image(img, caption="Your Work", use_container_width=True)

    # 4. The "Check" Button and AI Logic
    if st.button("Check My Solution"):
        with st.spinner("Analyzing your steps..."):
            prompt = """
            You are a Socratic Math Tutor. 
            Look at the image provided which contains a math problem and a student's solution.
            1. If the solution is 100% correct, celebrate the student!
            2. If there is a mistake, find the VERY FIRST step where the error occurred.
            3. DO NOT give the correct answer. 
            4. Provide a hint or ask a leading question that helps the student realize their mistake.
            """
            
            # Send the image and prompt to Gemini
            response = model.generate_content([prompt, img])
            
            st.markdown("### 📝 Tutor Feedback:")
            st.info(response.text)
