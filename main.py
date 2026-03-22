import os
import requests
import google.generativeai as genai

# 1. Setup APIs
# These names MUST match your GitHub Secrets exactly
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
BEEHIIV_KEY = os.environ["BEEHIIV_API_KEY"]
PUB_ID = os.environ["BEEHIIV_PUBLICATION_ID"]

def get_ai_analysis():
    # Using the stable 2026 workhorse model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = """
    Analyze today's top financial news for Gold and the S&P 500. 
    Provide a concise, 3-bullet point summary for a newsletter.
    Tone: Professional, witty, and data-driven.
    """
    
    try:
        response = model.generate_content(prompt)
        print("--- AI ANALYSIS GENERATED ---")
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        return None

def send_to_beehiiv(content):
    if not content:
        return

    # Beehiiv API v2 Endpoint
    url = f"https://api.beehiiv.com/v2/publications/{PUB_ID}/posts"
    
    headers = {
        "Authorization": f"Bearer {BEEHIIV_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": "Daily Market Pulse",
        "subtitle": "AI-Powered Market Insights",
        "body_content": f"<h3>Today's Analysis:</h3><p>{content.replace('', '<br>')}</p>",
        "status": "draft" 
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201 or response.status_code == 200:
            print("Successfully created Beehiiv draft!")
        else:
            print(f"Beehiiv Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    analysis = get_ai_analysis()
    send_to_beehiiv(analysis)
