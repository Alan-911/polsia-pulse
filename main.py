import os
from google.genai import Client  # Updated 2026 Import Path

def get_market_pulse():
    # 1. Initialize the Gemini Client
    try:
        # The SDK will automatically try to find your 'GEMINI_API_KEY'
        client = Client(api_key=os.environ.get("GEMINI_API_KEY"))
    except Exception as e:
        print(f"Auth Error: {e}")
        return

    # 2. Define your prompt
    prompt = "Analyze today's financial news for Gold and the S&P 500. Provide 3 witty bullet points."

    # 3. Generate content
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        
        print("--- DAILY MARKET PULSE ---")
        print(response.text)
        return response.text

    except Exception as e:
        print(f"AI Generation Error: {e}")

if __name__ == "__main__":
    get_market_pulse()
