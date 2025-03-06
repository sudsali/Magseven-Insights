import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
import yfinance as yf
import together

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
            hist = stock.history(period="1d") 
            if len(hist) == 0:
                return None 
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
                "tbm": "nws"
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
    def __init__(self):
        self.role = "Expert financial summarizer."
        self.context = "Generating concise, impactful summaries of financial news for informed investors."
        self.backstory = "I am a highly skilled financial analyst with a passion for making complex information accessible."
        
    def summarize(self, news_articles, company_name):
        if not news_articles:
            return "No significant news to summarize."
        try:
            text = ". ".join([f"{article['title']}. {article.get('snippet', 'No summary available')}" for article in news_articles])
        
            prompt = f"""
            You are a financial expert. Provide a concise, informative, and engaging summary (under 200 words) of the following news articles related to {company_name} stock. Focus on key findings, important metrics, potential impacts on the stock price, and overall market sentiment. The summary should be well structured, written in a style similar to Inshorts, and directly presentable in a financial newsletter. 
            
            For Example: 
            Bad Response:
            Tesla's stock has plummeted over 40% due to declining sales in China and poor German sales data. Despite this, there are 3 key reasons the stock is rising: overcoming bad sales data, strong brand loyalty, and innovative products. However, Elon Musk's net worth has dropped by $116 billion from its peak, and boardroom insider Robyn Denholm has added to the pain. Overall, the stock is facing a nightmare, but there are signs of resilience. With market sentiment being bearish, investors should be cautious, but also watch for potential buying opportunities.
            ```

            Note that the original response already meets the instruction to provide a concise summary under 200 words, and it effectively captures the key points from the news articles. The only issue identified was the unnecessary phrase at the beginning, which has been removed in the rewritten response.

            The rewritten response remains the same as the original response, as it has already been corrected to meet the instruction following standard:


            Tesla's stock has plummeted over 40% due to declining sales in China and poor German sales data. Despite this, there are 3 key reasons the stock is rising: overcoming bad sales data, strong brand loyalty, and innovative products. However, Elon Musk's net worth has dropped by $116 billion from its peak, and boardroom insider Robyn Denholm has added to the pain. Overall, the stock is facing a nightmare, but there are signs of resilience. With market sentiment being bearish, investors should be

            Good Response:

            Tesla's stock has plummeted over 40% due to declining sales in China and poor German sales data. Despite this, there are 3 key reasons the stock is rising: overcoming bad sales data, strong brand loyalty, and innovative products. However, Elon Musk's net worth has dropped by $116 billion from its peak, and boardroom insider Robyn Denholm has added to the pain. Overall, the stock is facing a nightmare, but there are signs of resilience. With market sentiment being bearish, investors should be cautious, but also watch for potential buying opportunities.


            Bad Response:
            Nvidia is poised to make significant gains in 2025, driven by promising developments. The company's stock is anticipated to soar, thanks to key announcements from CEO Jensen Huang. With a potential race to a $5 trillion valuation, Nvidia is competing with tech giant Apple. Preliminary market movements show Nvidia's stock on the rise, potentially signaling a perceived bargain. However, billionaire investor Stanley Druckenmiller has recently divested his Nvidia shares, opting for alternative AI investments. Overall, market sentiment remains optimistic, with many expecting Nvidia to make substantial strides in the AI sector, potentially impacting its stock price positively. 
            ```


            Nvidia is poised to make significant gains in 2025, driven by promising developments. The company's stock is anticipated to soar, thanks to key announcements from CEO Jensen Huang. With a potential race to a $5 trillion valuation, Nvidia is competing with tech giant Apple. Preliminary market movements show Nvidia's stock on the rise, potentially signaling a perceived bargain. However, billionaire investor Stanley Druckenmiller has recently divested his Nvidia shares, opting for alternative AI investments. Overall, market sentiment remains optimistic, with many expecting Nvidia to make substantial strides in the AI sector, potentially impacting its stock price positively.

            Good Response:
            Nvidia is poised to make significant gains in 2025, driven by promising developments. The company's stock is anticipated to soar, thanks to key announcements from CEO Jensen Huang. With a potential race to a $5 trillion valuation, Nvidia is competing with tech giant Apple. Preliminary market movements show Nvidia's stock on the rise, potentially signaling a perceived bargain. However, billionaire investor Stanley Druckenmiller has recently divested his Nvidia shares, opting for alternative AI investments. Overall, market sentiment remains optimistic, with many expecting Nvidia to make substantial strides in the AI sector, potentially impacting its stock price positively. 

            News Articles:
            {text}

            Respond with ONLY the summary and no other text.

            """
        
            response = together.Complete.create(
                prompt=prompt, 
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                max_tokens=300,
                temperature=0.7,
            )
        
            if isinstance(response, dict) and 'output' in response:
                summary = response['output']['choices'][0]['text'].strip()
            elif isinstance(response, dict) and 'choices' in response:
                summary = response['choices'][0]['text'].strip()
            else:
                summary = "Unable to generate summary due to unexpected API response format."
        
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
        return "Unable to generate summary at this time."

class SummaryEditorAgent:
    """Agent responsible for editing the newsletter to remove extra summaries."""
    def __init__(self):
        self.role = "Newsletter editor."
        self.context = "Removing extra summaries from the newsletter."
        self.backstory = ("I am an editor who understands when and where to cut copy for maximum efficiency. "
                          "I am only here to make the newsletter read right.")

    def remove_extra_summary(self, newsletter_content):
        """Removes extra summaries from the newsletter content using LLM."""
        try:
            prompt = f"""
                You are an expert newsletter editor.  You are provided with the content of a financial newsletter below. Your task is to remove any redundant or duplicate paragraphs that appear immediately after the "News Summary:" for each company.  Ensure that the core news summary is retained, and only the immediately following duplicated paragraph is removed. Preserve all other content and formatting.

                Newsletter Content:
                {newsletter_content}

                Respond with ONLY the cleaned newsletter content.
                """

            response = together.Complete.create(
                prompt=prompt,
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                max_tokens=2000,  
                temperature=0.7,
            )

            if isinstance(response, dict) and 'output' in response:
                cleaned_newsletter = response['output']['choices'][0]['text'].strip()
            elif isinstance(response, dict) and 'choices' in response:
                cleaned_newsletter = response['choices'][0]['text'].strip()
            else:
                cleaned_newsletter = newsletter_content 
                print("Unable to clean newsletter due to unexpected API response format.")

            return cleaned_newsletter

        except Exception as e:
            print(f"Error cleaning newsletter: {e}")
            return newsletter_content 

    def get_role(self):
        return self.role

    def get_context(self):
        return self.context

    def get_backstory(self):
        return self.backstory