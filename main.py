import os
import requests
import google.generativeai as genai

# 1. Setup API Keys
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    BEEHIIV_KEY = os.environ["BEEHIIV_API_KEY"]
    PUB_ID = os.environ["BEEHIIV_PUBLICATION_ID"]
except KeyError as e:
    print(f"Error: Missing GitHub Secret {e}")
    exit(1)

def get_ai_analysis():
    # Stable 2026 model name
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = "Analyze today's Gold and S&P 500 news. 3 witty bullets for a newsletter."
    try:
        response = model.generate_content(prompt)
        print("--- AI ANALYSIS GENERATED ---")
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        return None

def send_to_beehiiv(content):
    if not content: return
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
    analysis = get_ai_analysis()
    send_to_beehiiv(analysis)
