import os
import requests
from google import genai

def get_market_news():
    news_key = os.environ.get("NEWS_API_KEY")
    # Using 'OR' to ensure we always get headlines for either Gold or S&P 500
    url = f"https://newsapi.org/v2/everything?q=Gold+OR+S%26P500&language=en&sortBy=publishedAt&apiKey={news_key}"
    try:
        res = requests.get(url).json()
        articles = res.get('articles', [])[:5]
        headlines = "\n".join([f"- {a['title']}" for a in articles])
        return headlines if headlines else "Markets are steady today."
    except Exception as e:
        print(f"NewsAPI Error: {e}")
        return "Market data is currently being processed."

def run_polsia():
    # Secrets from GitHub Environment
    gem_key = os.environ.get("GEMINI_API_KEY")
    bee_key = os.environ.get("BEEHIIV_API_KEY")
    pub_id = os.environ.get("BEEHIIV_PUBLICATION_ID")
    
    # 1. Fetch Real Headlines
    headlines = get_market_news()
    print(f"--- HEADLINES FETCHED ---\n{headlines}\n")

    # 2. AI Analysis via Gemini
    client = genai.Client(api_key=gem_key)
    try:
        prompt = f"Using these real headlines:\n{headlines}\n\nWrite 3 witty, professional bullets for a financial newsletter. Keep it punchy."
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        analysis = response.text

        # 3. Post to Beehiiv as a Draft
        url = f"https://api.beehiiv.com/v2/publications/{pub_id}/posts"
        headers = {
            "Authorization": f"Bearer {bee_key}", 
            "Content-Type": "application/json"
        }
        data = {
            "title": "Daily Market Pulse",
            "body_content": f"<p>{analysis}</p>",
            "status": "draft"
        }
        
        post_res = requests.post(url, headers=headers, json=data)
        
        print(f"--- BEEHIIV STATUS ---")
        print(f"Status Code: {post_res.status_code}")
        print(f"Response: {post_res.text}")

        if post_res.status_code in [200, 201]:
            print("🚀 SUCCESS: Draft created in Beehiiv!")
        else:
            print("❌ FAILED: Check your Publication ID and API Key.")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")

if __name__ == "__main__":
    run_polsia()
