import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")  # Replace this

models = genai.list_models()

print("Available models:")
for m in models:
    print("-", m.name)
