import os
import requests
from google import genai

# 1. Setup APIs
# Ensure these 3 names exist in your GitHub Secrets!
GENAI_KEY = os.environ.get("GEMINI_API_KEY")
BEEHIIV_KEY = os.environ.get("BEEHIIV_API_KEY")
PUB_ID = os.environ.get("BEEHIIV_PUBLICATION_ID")

def get_ai_analysis():
    client = genai.Client(api_key=GENAI_KEY)
    prompt = "Analyze today's Gold and S&P 500 news. 3 witty bullets for a newsletter."
    
    try:
        # Using the newest 2026 stable model
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        print("--- AI ANALYSIS GENERATED ---")
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        return None

def send_to_beehiiv(content):
    if not content or not PUB_ID:
        print("Error: Missing content or Publication ID")
        return

    url = f"https://api.beehiiv.com/v2/publications/{PUB_ID}/posts"
    headers = {
        "Authorization": f"Bearer {BEEHIIV_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": "Daily Market Pulse",
        "subtitle": "AI-Powered Market Insights",
        "body_content": f"<h3>Today's Analysis:</h3><p>{content}</p>",
        "status": "draft" 
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print("Successfully created Beehiiv draft!")
    else:
        print(f"Beehiiv Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if not all([GENAI_KEY, BEEHIIV_KEY, PUB_ID]):
        print("Error: One or more GitHub Secrets are missing!")
    else:
        analysis = get_ai_analysis()
        send_to_beehiiv(analysis)
