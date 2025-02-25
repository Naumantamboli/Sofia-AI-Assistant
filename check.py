import google.generativeai as genai

# Configure API Key
genai.configure(api_key="AIzaSyCAlGGqqxotMGYOEBBrf9E_FDkU-ZC0Ucc")  # Replace with your actual API key

# List available models
models = genai.list_models()

# Print model names
for model in models:
    print(model.name)
