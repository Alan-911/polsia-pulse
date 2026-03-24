import os
import requests
from google import genai

def run_polsia():
    # 1. Fetching Credentials
    gem_key = os.environ.get("GEMINI_API_KEY")
    bee_key = os.environ.get("BEEHIIV_API_KEY")
    pub_id = os.environ.get("BEEHIIV_PUBLICATION_ID")

    # 2. AI Content Generation
    client = genai.Client(api_key=gem_key)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Summarize today's Gold and S&P 500 news in 3 witty bullets."
        )
        analysis = response.text
        print("✅ Gemini Analysis Complete.")

        # 3. Beehiiv API Delivery (Force-Visible Version)
        url = f"https://api.beehiiv.com/v2/publications/{pub_id}/posts"
        headers = {
            "Authorization": f"Bearer {bee_key}", 
            "Content-Type": "application/json"
        }
        
        data = {
            "title": "Daily Market Pulse",
            "body_content": f"<p>{analysis}</p>",
            "status": "draft",
            "publish_to_web": True,  # Ensures it shows in the dashboard list
            "send_email": False      # Keeps it as a draft, doesn't send yet
        }
        
        res = requests.post(url, headers=headers, json=data)
        
        if res.status_code in [200, 201]:
            post_id = res.json().get('data', {}).get('id')
            print(f"🚀 SUCCESS! Post created with ID: {post_id}")
        else:
            print(f"❌ Beehiiv Error {res.status_code}: {res.text}")
            
    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    run_polsia()
