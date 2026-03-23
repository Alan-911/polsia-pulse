import os
import requests
import sys
try:
    from google import genai
except ImportError:
    print("❌ ERROR: 'google-genai' not installed. Please check requirements.txt")
    sys.exit(1)

# --- CONFIGURATION ---
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
BEEHIIV_KEY = os.environ.get("BEEHIIV_API_KEY")
PUB_ID = os.environ.get("BEEHIIV_PUBLICATION_ID")

def run_automation():
    # 1. Start Gemini Client
    client = genai.Client(api_key=GEMINI_KEY)
    
    # 2. Generate Content
    prompt = "Provide a 3-bullet witty summary of today's Gold and S&P 500 trends for a financial newsletter."
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        analysis = response.text
        print("✅ AI analysis generated successfully.")

        # 3. Post to Beehiiv
        url = f"https://api.beehiiv.com/v2/publications/{PUB_ID}/posts"
        headers = {
            "Authorization": f"Bearer {BEEHIIV_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "title": "Daily Market Pulse",
            "body_content": f"<p>{analysis}</p>",
            "status": "draft"
        }

        res = requests.post(url, headers=headers, json=payload)
        if res.status_code in [200, 201]:
            print("🚀 SUCCESS: Newsletter draft created in Beehiiv!")
        else:
            print(f"❌ Beehiiv Error {res.status_code}: {res.text}")

    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    # Safety Check for Secrets
    missing = [k for k, v in {"GEMINI_API_KEY": GEMINI_KEY, "BEEHIIV_API_KEY": BEEHIIV_KEY, "BEEHIIV_PUBLICATION_ID": PUB_ID}.items() if not v]
    if missing:
        print(f"❌ CRITICAL ERROR: Missing GitHub Secrets: {', '.join(missing)}")
        print("Go to Settings > Secrets > Actions to add them.")
        sys.exit(1)
    
    run_automation()
