import os
from dotenv import load_dotenv
from agents import StockDataAgent, NewsAgent, SummaryAgent

# Load environment variables from .env file
load_dotenv()

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

def generate_company_update(company_name, stock_symbol):
    """Generates a company update string with stock data and news summary."""
    stock_data_agent = StockDataAgent(stock_symbol)
    stock_data = stock_data_agent.get_stock_data()

    news_agent = NewsAgent(company_name, stock_symbol)
    news_articles = news_agent.fetch_news_articles()[:5]

    summary_agent = SummaryAgent()
    news_summary = summary_agent.summarize(news_articles, company_name)

    if stock_data:
        closing_price = stock_data["closing_price"]
        change_percent = stock_data["change_percent"]

        update = (
            f"**{company_name} ({stock_symbol}):**\n"
            f"Today's Closing Price: ${closing_price:.2f}\n"
            f"Change Percent: {change_percent:.2f}%\n"
            f"News Summary: {news_summary}\n\n"
        )
        return update
    else:
        return f"Could not retrieve data for {company_name} ({stock_symbol})\n\n"