import os
import requests
from google import genai

# Pulling the 'Keys' to the business from GitHub Secrets
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
BEEHIIV_KEY = os.environ.get("BEEHIIV_API_KEY")
PUB_ID = os.environ.get("BEEHIIV_PUBLICATION_ID")

def run_polsia_pulse():
    # 1. AI Analysis Phase (Using the modern 2026 client)
    client = genai.Client(api_key=GEMINI_KEY)
    prompt = "Analyze today's Gold and S&P 500 news. Provide 3 witty, professional bullets."
    
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        content = response.text
        print("✅ AI Analysis Complete")
        
        # 2. Beehiiv Delivery Phase
        url = f"https://api.beehiiv.com/v2/publications/{PUB_ID}/posts"
        headers = {
            "Authorization": f"Bearer {BEEHIIV_KEY}", 
            "Content-Type": "application/json"
        }
        data = {
            "title": "Daily Market Pulse",
            "body_content": f"<p>{content}</p>",
            "status": "draft"
        }
        
        res = requests.post(url, headers=headers, json=data)
        if res.status_code in [200, 201]:
            print("🚀 Success! Draft created in Beehiiv.")
        else:
            print(f"❌ Beehiiv Error: {res.status_code} - {res.text}")
            
    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    # Internal Debugger: Checks for missing Secrets before running
    missing = [name for name, val in [("GEMINI_API_KEY", GEMINI_KEY), ("BEEHIIV_API_KEY", BEEHIIV_KEY), ("BEEHIIV_PUBLICATION_ID", PUB_ID)] if not val]
    if missing:
        print(f"CRITICAL: Missing Secrets in GitHub Settings: {', '.join(missing)}")
    else:
        run_polsia_pulse()
