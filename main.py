import os
from google import genai

def get_market_pulse():
    # 1. Initialize the Gemini Client
    # It will automatically look for 'GEMINI_API_KEY' in your GitHub Secrets
    try:
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    except KeyError:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return

    # 2. Define your prompt (The instructions for the AI)
    prompt = """
    You are a professional Market Analyst for 'The Pulse'. 
    Analyze today's top financial news specifically focusing on Gold, Oil, and the S&P 500.
    Provide a concise, 3-bullet point summary that is ready for a newsletter.
    Tone: Professional, witty, and data-driven.
    """

    # 3. Generate the content using the 2026 Free Workhorse Model
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )
        
        # 4. Print the result (This shows up in your GitHub Action logs)
        print("--- DAILY MARKET PULSE ---")
        print(response.text)
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_market_pulse()

