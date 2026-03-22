import os
import google.generativeai as genai

# 1. Setup the connection
# Make sure your GitHub Secret is named GEMINI_API_KEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_market_pulse():
    # 2. Choose the 2026 stable model
    # (gemini-2.5-flash is the current free-tier workhorse)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = """
    Analyze today's top financial news for Gold and the S&P 500. 
    Provide a concise, 3-bullet point summary for a newsletter.
    Tone: Professional and witty.
    """

    # 3. Generate and Print
    try:
        response = model.generate_content(prompt)
        print("--- DAILY MARKET PULSE ---")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_market_pulse()
