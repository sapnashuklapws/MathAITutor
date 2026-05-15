import google.generativeai as genai

# Use your actual key here
genai.configure(api_key="YOUR_API_KEY")

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
