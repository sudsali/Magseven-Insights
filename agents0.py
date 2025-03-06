import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
import yfinance as yf
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import requests
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

class StockDataAgent:
    """Agent responsible for fetching stock data."""
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self.role = "Fetching real-time stock data."
        self.context = f"Stock symbol: {stock_symbol}"
        self.backstory = "This agent has a long history of fetching stock prices and analyzing trends based on Yahoo Finance API."

    def get_stock_data(self):
        """Fetches stock data for a given stock symbol."""
        try:
            stock = yf.Ticker(self.stock_symbol)
            hist = stock.history(period="1d")  # Fetch today's data
            if len(hist) == 0:
                return None  # Not enough data
            closing_price = hist['Close'].iloc[-1]
            # Calculate change from yesterday's closing price
            hist = stock.history(period="2d")
            if len(hist) < 2:
                previous_closing_price = closing_price
                change_percent = 0
            else:
                previous_closing_price = hist['Close'].iloc[-2]
                change_percent = ((closing_price - previous_closing_price) / previous_closing_price) * 100
            return {
                "closing_price": closing_price,
                "change_percent": change_percent
            }
        except Exception as e:
            print(f"Error fetching stock data for {self.stock_symbol}: {e}")
            return None

    def get_role(self):
        return self.role

    def get_context(self):
        return self.context

    def get_backstory(self):
        return self.backstory

class NewsAgent:
    """Agent responsible for fetching news articles related to a company."""
    def __init__(self, company_name, stock_symbol):
        self.company_name = company_name
        self.stock_symbol = stock_symbol
        self.role = "Fetching the latest news articles for the given company."
        self.context = f"Company: {company_name}, Stock Symbol: {stock_symbol}"
        self.backstory = "This agent is skilled in using SerpAPI to retrieve the most up-to-date news articles related to stock markets."
        self.api_key = os.getenv("SERPAPI_KEY")

    def fetch_news_articles(self):
        """Fetches news articles related to the company using SerpAPI."""
        try:
            search_params = {
                "q": f"{self.company_name} stock news",
                "api_key": self.api_key,
                "engine": "google_news",
                "tbm": "nws" # Focus on just google news
            }
            search = GoogleSearch(search_params)
            results = search.get_dict()
            articles = results.get("news_results", [])
            return articles
        except Exception as e:
            print(f"Error fetching news for {self.company_name}: {e}")
            return []

    def get_role(self):
        return self.role

    def get_context(self):
        return self.context

    def get_backstory(self):
        return self.backstory

class SummaryAgent:
    """Agent responsible for summarizing news articles using GPT-2 after understanding the article content."""
    def __init__(self):
        self.role = "Expert financial summarizer."
        self.context = "Generating concise, impactful summaries of financial news for informed investors."
        self.backstory = "I am a highly skilled financial analyst with a passion for making complex information accessible. I leverage GPT-2 to provide insightful and engaging summaries."
        try:
            self.model = GPT2LMHeadModel.from_pretrained("gpt2")
            self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
        except Exception as e:
            print(f"Error initializing GPT-2: {e}")
            self.model = None
            self.tokenizer = None
            self.device = None

    def summarize(self, news_articles, company_name):
        """Summarizes the news articles using GPT-2."""
        if not news_articles or not self.model or not self.tokenizer:
            return "No significant news to summarize."
        try:
            # Combine titles and snippets of relevant articles and truncate
            text = ". ".join([f"{article['title']}. {article.get('snippet', 'No summary available')}" for article in news_articles])
            

            # Craft a detailed prompt using advanced techniques
            prompt = f"""
            As a seasoned financial analyst, create a concise, informative, and engaging summary of the following news articles related to {company_name} stock. Your summary should:

            1.  Be no more than 200 words.
            2.  Highlight key findings and important metrics (e.g., revenue, profit, market share).
            3.  Identify potential impacts on the stock price (positive, negative, or neutral).
            4.  Convey the overall market sentiment towards the stock.
            5.  Be written in a style similar to Inshorts, making complex information accessible to a broad audience.
            6. Adopt the persona of an expert investor.
            7. Include information relevent to investors

            Articles:
            {text}

            Summary:
            """

            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=700).to(self.device) # made the input size 700
            outputs = self.model.generate(
                inputs,
                max_new_tokens=300,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                do_sample=True,
                temperature=0.7,
                attention_mask=torch.ones(inputs.shape).to(self.device),
                pad_token_id=self.tokenizer.eos_token_id
            )
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            summary = summary.replace(prompt, "").strip()

            return summary

        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Unable to generate summary at this time."

    def get_role(self):
        return self.role

    def get_context(self):
        return self.context

    def get_backstory(self):
        return self.backstory