import os
from dotenv import load_dotenv
from google import genai
from PIL import Image  # IMPORTANTE: Libreria per aprire le immagini

# 1. Load the secret key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Error: API Key not found in the .env file!")

client = genai.Client(api_key=API_KEY)

print("System ready. Loading ad assets (Image + Text)...\n")

# 2. Load the Ad Copy (Text)
with open("ad_copy.txt", "r", encoding="utf-8") as file:
    ad_text = file.read()

# 3. Load the Ad Image
try:
    ad_image = Image.open("ad_image.jpg")
except FileNotFoundError:
    raise FileNotFoundError("Error: 'ad_image.jpg' not found in the folder!")

# 4. The Expert Marketing Prompt
system_prompt = (
    "You are an expert Digital Marketing Consultant specializing in Meta Ads (Facebook/Instagram). "
    "Analyze the provided ad image and its accompanying text copy together. "
    "Provide a sharp, structured evaluation report.\n\n"
    "Please format your response strictly as follows:\n"
    "1. SCORE: [Rate from 1 to 10 based on conversion potential]\n"
    "2. STRENGTHS: [1 short sentence on what works well]\n"
    "3. WEAKNESSES: [1 short sentence on what could be better]\n"
    "4. ACTIONABLE ADVICE: [1 specific tip to increase the Click-Through Rate]"
)

print("Sending Multimodal data to Gemini AI...")
print("Please wait...\n")

# 5. Send both Image and Text to the AI in a single request
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[system_prompt, ad_image, f"Ad Copy: '{ad_text}'"]
)

# 6. Print the results
print("--- 📊 MARKETING EVALUATION REPORT ---")
print(response.text)