from tools import generate_company_update
from agents import NewsAgent, SummaryAgent
import yfinance as yf  
from datetime import datetime
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
# List of Magnificent Seven Stocks
MAGNIFICENT_SEVEN = ["Apple", "Microsoft", "Amazon", "Alphabet", "Meta", "Nvidia", "Tesla"]
COMPANY_TICKER_MAP = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
    "Nvidia": "NVDA",
    "Tesla": "TSLA"
}

def get_etf_data(etf_symbol):
    """Fetches ETF data using yfinance."""
    try:
        etf = yf.Ticker(etf_symbol)
        hist = etf.history(period="1d")  # Fetch todays data
        if len(hist) == 0:
            return None
        closing_price = hist['Close'].iloc[-1]
        previous_closing_price = hist['Close'].iloc[-1]
        change_percent = ((closing_price - previous_closing_price) / previous_closing_price) * 100
        return {
            "closing_price": closing_price,
            "change_percent": change_percent
        }
    except Exception as e:
        print(f"Error fetching ETF data for {etf_symbol}: {e}")
        return None

def fetch_magnificent_seven_news():
    """Fetches news specifically about the Magnificent Seven as a whole."""
    api_key = os.getenv("SERPAPI_KEY")
    try:
        search_params = {
            "q": "Magnificent Seven stock news",
            "api_key": api_key,
            "engine": "google_news",
             "tbm": "nws" 
        }
        search = GoogleSearch(search_params)
        results = search.get_dict()
        articles = results.get("news_results", [])
        return articles
    except Exception as e:
        print(f"Error fetching news for Magnificent Seven: {e}")
        return []

def generate_newsletter(company_updates):
    """Generates a professional financial newsletter."""
    # Fetch ETF Data
    etf_data = get_etf_data("MAGS")  
    magnificent_seven_news = fetch_magnificent_seven_news()

    # Create summary agent
    summary_agent = SummaryAgent()
    magnificent_seven_summary = summary_agent.summarize(magnificent_seven_news, "Magnificent Seven") #Added compnay name

    # Create a structured, engaging format for the newsletter
    newsletter_content = f"**Today's ({current_time}) Stock Market Update: The Magnificent Seven (MAGS)**\n\n"

    # Add ETF data to the beginning of the newsletter

    newsletter_content += "Hello Investors,\n\n"
    newsletter_content += "Here's the latest market movement of the Magnificent Seven stocks:\n\n"
    newsletter_content += f"**Magnificent Seven (Overall):**\n\n"
    etf_intro = ""
    if etf_data:
        change_percent = etf_data['change_percent']
        etf_intro = (
            f"**Roundhill Magnificent Seven ETF (BATS: MAGS)**\n"
            f"Today's Closing Price: ${etf_data['closing_price']:.2f}\n"
            f"Change Percent: {change_percent:.2f}%\n"
            f"News Summary: {magnificent_seven_summary}\n\n"
        )
    newsletter_content += etf_intro

    for update in company_updates:
        newsletter_content += update

    # Closing remarks
    newsletter_content += "Stay tuned for more updates.\n\n"
    newsletter_content += "- **The Magnificent Seven Insider**\n"

    return newsletter_content

def fetch_news_task():
    """Fetches the latest news on the Magnificent Seven stocks."""
    news_items = []
    for company_name, stock_symbol in COMPANY_TICKER_MAP.items():
        # Create NewsAgent instance for each company and fetch the latest news articles
        news_agent = NewsAgent(company_name, stock_symbol)
        news = news_agent.fetch_news_articles()
        news_items.extend(news)
    return news_items