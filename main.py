import os
import requests
from google import genai
from datetime import datetime, timedelta

def get_market_news():
    news_key = os.environ.get("NEWS_API_KEY")
    # Querying both Gold and S&P 500
    url = f"https://newsapi.org/v2/everything?q=Gold+OR+S%26P500&language=en&sortBy=publishedAt&apiKey={news_key}"
    try:
        res = requests.get(url).json()
        articles = res.get('articles', [])[:5]
        headlines = [a['title'] for a in articles if len(a['title']) > 10]
        return headlines
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def run_polsia():
    gem_key = os.environ.get("GEMINI_API_KEY")
    bee_key = os.environ.get("BEEHIIV_API_KEY")
    pub_id = os.environ.get("BEEHIIV_PUBLICATION_ID")
    
    # --- STEP 1: SELF-CORRECTION CHECK ---
    headlines = get_market_news()
    
    if not headlines:
        print("⚠️ SELF-CORRECTION: No high-quality news found. Polsia is skipping today's post to maintain quality.")
        return

    print(f"✅ Found {len(headlines)} headlines. Proceeding with analysis...")
    formatted_headlines = "\n".join([f"- {h}" for h in headlines])

    # --- STEP 2: BRAIN (GEMINI) ---
    client = genai.Client(api_key=gem_key)
    prompt = f"""
    Analyze these market headlines for today:
    {formatted_headlines}
    
    1. Assign a Market Mood emoji (🐂, 🐻, or ⚖️).
    2. Write 3 witty, professional insights for a financial newsletter.
    3. Return ONLY the HTML content (no ```html tags).
    """
    
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        analysis_html = response.text

        # --- STEP 3: AUTO-SCHEDULING (1 HOUR FROM NOW) ---
        publish_time = (datetime.now() + timedelta(hours=1)).isoformat()

        url = f"[https://api.beehiiv.com/v2/publications/](https://api.beehiiv.com/v2/publications/){pub_id}/posts"
        headers = {"Authorization": f"Bearer {bee_key}", "Content-Type": "application/json"}
        
        data = {
            "title": f"Market Pulse: {datetime.now().strftime('%B %d, %Y')}",
            "body_content": analysis_html,
            "status": "scheduled", 
            "publish_date": publish_time
        }
        
        post_res = requests.post(url, headers=headers, json=data)
        
        if post_res.status_code in [200, 201]:
            print(f"🚀 SUCCESS: Polsia has scheduled the post for {publish_time}")
        else:
            print(f"❌ ERROR: Beehiiv rejected the post. Status: {post_res.status_code}")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")

if __name__ == "__main__":
    run_polsia()
