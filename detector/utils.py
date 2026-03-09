import json

import google.generativeai as genai
from PIL import Image
import io

# 1. Configuration
# Ensure your API Key is correctly set
API_KEY = "AIzaSyB-j_KXiCWSYvV59e2KFppSIzge_uNF4QE" 


# Set your key securely
genai.configure(api_key=API_KEY)

def analyze_plant_with_json(image_bytes):
    """Identifies disease and returns structured data using Gemini 2.5 Flash."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # We ask Gemini to respond in JSON format
    prompt = (
        "Analyze this plant image. Provide the following in JSON format: "
        "\n- 'disease_name': The specific name of the disease or 'Healthy'."
        "\n- 'report': A detailed agricultural report with Overview, Treatment, and Prevention."
    )
    
    image_part = {"mime_type": "image/jpeg", "data": image_bytes}
    
    # Enable JSON mode in the generation config
    response = model.generate_content(
        [prompt, image_part],
        generation_config={"response_mime_type": "application/json"}
    )
    
    # Parse the string response into a Python dictionary
    return json.loads(response.text)