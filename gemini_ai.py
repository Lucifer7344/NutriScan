# gemini_ai.py

import google.generativeai as genai

#  Replace with your valid Gemini API Key
GEMINI_API_KEY = "AIzaSyCiVD6HRC7e4fIfQ6aWCAfgVGS5vq4jf6w"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini se jawab nahi mil paaya. Error: {e}"
