import os
import requests
from google import genai

def get_market_news():
    news_key = os.environ.get("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q=Gold+OR+S%26P500&language=en&sortBy=publishedAt&apiKey={news_key}"
    try:
        res = requests.get(url).json()
        articles = res.get('articles', [])[:5]
        return "\n".join([f"- {a['title']}" for a in articles])
    except:
        return "Market data stable."

def run_polsia():
    gem_key = os.environ.get("GEMINI_API_KEY")
    bee_key = os.environ.get("BEEHIIV_API_KEY")
    pub_id = os.environ.get("BEEHIIV_PUBLICATION_ID")
    
    headlines = get_market_news()
    client = genai.Client(api_key=gem_key)
    
    try:
        prompt = f"Using these headlines: {headlines}. Write 3 witty bullets for a newsletter."
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        analysis = response.text

        url = f"https://api.beehiiv.com/v2/publications/{pub_id}/posts"
        headers = {"Authorization": f"Bearer {bee_key}", "Content-Type": "application/json"}
        data = {
            "title": "Daily Market Pulse",
            "body_content": f"<p>{analysis}</p>",
            "status": "draft"
        }
        
        post_res = requests.post(url, headers=headers, json=data)
        print(f"DEBUG: Status {post_res.status_code}")
        print(f"DEBUG: Response {post_res.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_polsia()
