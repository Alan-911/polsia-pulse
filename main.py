import os
from google import genai  # Correct import for 2026 SDK

def get_market_pulse():
    # 1. Initialize the Gemini Client
    try:
        # The new SDK looks for 'GOOGLE_API_KEY' or you can pass it manually
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    except Exception as e:
        print(f"Auth Error: {e}")
        return

    # 2. Define your prompt
    prompt = "Analyze today's top financial news for Gold and the S&P 500. Provide 3 witty bullet points."

    # 3. Generate using the stable 2026 model
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        print("--- DAILY MARKET PULSE ---")
        print(response.text)
        return response.text

    except Exception as e:
        print(f"AI Generation Error: {e}")

if __name__ == "__main__":
    get_market_pulse()
