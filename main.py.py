import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gemini Model Finder")

st.title("🔎 Gemini Model Diagnostic Tool")
st.write("Use this tool to see exactly which models your API key has access to.")

# --- API Key Setup ---
# Checks Streamlit Cloud Secrets first, then sidebar input
api_key = st.secrets.get("GEMINI_API_KEY")

with st.sidebar:
    st.header("Settings")
    if not api_key:
        api_key = st.text_input("Enter your Gemini API Key:", type="password")
        st.info("Get a key at [Google AI Studio](https://aistudio.google.com/)")
    else:
        st.success("API Key loaded from Secrets!")

# --- Diagnostic Logic ---
if st.button("List My Available Models"):
    if not api_key:
        st.error("Please provide an API Key in the sidebar or Secrets.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Fetch the list of models
            model_list = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_list.append(m.name)
            
            if model_list:
                st.subheader("Compatible Models Found:")
                st.write("Copy the exact string below into your code:")
                for model_name in model_list:
                    st.code(model_name)
                    
                # Troubleshooting logic for your specific error
                if "models/gemini-1.5-flash" not in model_list:
                    st.warning("⚠️ 'gemini-1.5-flash' was NOT found in your list. This explains the 404 error.")
            else:
                st.warning("No models found that support 'generateContent'. Check if your API key is restricted.")
                
        except Exception as e:
            st.error(f"Failed to connect to Gemini API: {e}")

st.divider()
st.info("Note: Models usually appear as 'models/gemini-1.5-flash'. If you see 'models/gemini-pro', use that instead.")
