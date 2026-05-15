import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Math Solver", layout="wide")

st.title("🔢 Universal Math Solver")

# --- API Key Management ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # --- AUTO-DETECT BEST MODEL ---
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # Logic to pick the best model available to YOUR key
    # We prefer 1.5-flash because it usually has a free quota, unlike 2.0 in some regions
    target_model = None
    for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro-vision']:
        if preferred in available_models:
            target_model = preferred
            break
    
    if not target_model and available_models:
        target_model = available_models[0] # Fallback to whatever is first

    st.sidebar.success(f"Using Model: {target_model}")
    
    # --- UI Logic ---
    uploaded_file = st.file_uploader("Upload a photo of your math problem", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(img, caption="Your Image", use_container_width=True)
            
        if st.button("Check Math"):
            if not target_model:
                st.error("No compatible models found for this API key.")
            else:
                try:
                    with st.spinner('AI is analyzing...'):
                        model = genai.GenerativeModel(target_model)
                        prompt = "Look at this math problem. Identify it and check if the solution is correct. If wrong, explain why and give the correct step-by-step solution using LaTeX."
                        response = model.generate_content([prompt, img])
                        
                        with col2:
                            st.subheader("Analysis")
                            st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
                    if "Quota" in str(e):
                        st.info("Your region might have a 'Limit 0' quota for this model. Try a different API key or a VPN set to USA.")
else:
    st.warning("Please enter your API Key in the sidebar.")
