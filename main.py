import os
import requests
from google import genai

def run_polsia():
    gem_key = os.environ.get("GEMINI_API_KEY")
    bee_key = os.environ.get("BEEHIIV_API_KEY")
    pub_id = os.environ.get("BEEHIIV_PUBLICATION_ID")

    client = genai.Client(api_key=gem_key)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Summarize Gold and S&P 500 news in 3 witty bullets."
        )
        analysis = response.text

        url = f"https://api.beehiiv.com/v2/publications/{pub_id}/posts"
        headers = {"Authorization": f"Bearer {bee_key}", "Content-Type": "application/json"}
        
        data = {
            "title": "Daily Market Pulse Test",
            "body_content": f"AI Analysis: {analysis}",
            "status": "draft"
        }
        
        print(f"DEBUG: Attempting to post to Pub ID: {pub_id}")
        res = requests.post(url, headers=headers, json=data)
        
        # This will tell us if it's a 401 (Auth error) or 404 (ID error)
        print(f"DEBUG: Status Code: {res.status_code}")
        print(f"DEBUG: Response Text: {res.text}")

        if res.status_code in [200, 201]:
            print("🚀 SUCCESS! It should be in Beehiiv now.")
        else:
            print("❌ FAILURE: Beehiiv received the request but rejected it.")
            
    except Exception as e:
        print(f"❌ SYSTEM CRASH: {e}")

if __name__ == "__main__":
    run_polsia()
