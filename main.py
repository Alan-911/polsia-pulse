import requests
import google.generativeai as genai

# Setup your keys here
NEWS_API_KEY = "YOUR_NEWS_API_KEY"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

def get_market_pulse():
    # 1. Fetch live news about Gold and Macro economics
    url = f"https://newsapi.org/v2/everything?q=gold market OR inflation&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get('articles', [])[:5]
    
    context = "\n".join([f"- {a['title']}: {a['description']}" for a in articles])
    
    # 2. Use Gemini to analyze and write the "Pulse"
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Analyze these news items for a gold investor. Write a 3-bullet executive summary (Trend, Risk, Action): \n\n{context}"
    
    report = model.generate_content(prompt)
    return report.text

if __name__ == "__main__":
    report = get_market_pulse()
    print("--- TODAY'S PULSE ---")
    print(report)
    # Next step: Send this to Beehiiv/Email

import requests

def publish_to_beehiiv(title, content_html):
    """Publishes the AI report directly to your Beehiiv newsletter."""
    
    API_KEY = "YOUR_BEEHIIV_API_KEY"
    PUB_ID = "YOUR_PUBLICATION_ID"
    
    url = f"https://api.beehiiv.com/v2/publications/{PUB_ID}/posts"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": title,
        "subtitle": "Daily AI-Driven Market Pulse",
        "content": content_html, # You can send raw HTML here
        "publish_status": "draft", # Change to 'confirmed' to send immediately!
        "send_email": True,
        "display_on_web": True
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        print("🚀 Post created successfully on Beehiiv!")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")