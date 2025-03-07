# MagSeven Insights: AI-Powered Financial Newsletter Generator

## Overview

MagSeven Insights is an innovative AI-driven financial newsletter generator that leverages Large Language Models (LLMs) to provide real-time analysis of the news related to 'Magnificent Seven' tech stocks: Apple, Microsoft, Amazon, Alphabet, Meta, Nvidia, and Tesla.

## Features

- Real-time stock data integration using yfinance API
- Automated news aggregation via SerpAPI
- AI-powered summarization using the Llama-3.3-70B-Instruct-Turbo-Free model
- Custom-built agents for data fetching, news analysis, and content refinement
- Daily newsletter generation with concise, informative updates on each stock

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/magseven-insights.git
   cd magseven-insights
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   SERPAPI_KEY=your_serpapi_key_here
   TOGETHER_API_KEY=your_together_ai_key_here
   ```

## Usage

Run the main script to generate the newsletter:

```
python main.py
```

## Project Structure

- `main.py`: Entry point of the application
- `agents.py`: Contains agent classes for stock data, news fetching, and summarization
- `tools.py`: Utility functions for generating company updates
- `tasks.py`: Task functions for fetching news and generating the newsletter

## Previous Iterations
`agents0.py`: An earlier version of the agent system that attempted to use the GPT-2 model by HuggingFace for summarization. This file demonstrates the project's evolution and experimentation with different language models. While it didn't achieve the desired results, it serves as a valuable reference for the development process and the decision to switch to the current model used in agents.py.

## Demo Output

```
Gathering latest news on the Magnificent Seven stocks...

**Today's (2025-03-06 13:14:26) Stock Market Update: The Magnificent Seven (MAGS)**

Hello Investors,

Here's the latest market movement of the Magnificent Seven stocks:

**Magnificent Seven (Overall):**

**Roundhill Magnificent Seven ETF (BATS: MAGS)**
Today's Closing Price: $48.95
Change Percent: 0.00%
News Summary: The Magnificent Seven stocks, comprising tech giants like Nvidia, Meta, and Tesla, have experienced a decline in recent times. Despite this, some analysts believe that certain stocks within this group, such as Meta, are poised for a rebound. The market sentiment remains cautious, with investors advised to be selective in their investments. Key metrics, including valuation and earnings growth, will be crucial in determining the future performance of these stocks. As the tech sector continues to evolve, the Magnificent Seven stocks will likely face increased competition from emerging players in the AI and quantum computing spaces. Investors should remain vigilant and consider diversifying their portfolios to mitigate potential risks. With the emergence of new technologies and shifting market trends, the Magnificent Seven stocks may need to adapt to maintain their dominance.

**Apple (AAPL):**
Today's Closing Price: $234.83
Change Percent: -0.39%
News Summary: Apple's stock is under scrutiny ahead of its product launch, with analysts weighing the pros and cons. Warren Buffett continues to hold his Apple stock, indicating confidence. Meanwhile, Jim Cramer questions the potential impact of China-related policies on Apple. The company's $500 billion investment in America has sparked interest, with some considering the stock a buy. Overall, market sentiment is mixed, with investors watching for the product launch and its potential impact on the stock price. With key metrics and analyst opinions in focus, Apple's stock is poised for significant movement, making it essential for investors to stay informed.

**Microsoft (MSFT):**
Today's Closing Price: $397.43
Change Percent: -0.89%
News Summary: Microsoft's stock has retaken the $400 level, prompting investors to consider whether it's a buy or sell in March. Meanwhile, a large MSFT stockholder is a strong advocate for crypto and blockchain, despite Microsoft missing out on Bitcoin investments. The stock has hit its lowest level in over a year, but some analysts believe the selloff may be overdone. With five key reasons to support a strong buy, and the stock hitting new 52-week lows, investors may find it an attractive opportunity to snap up MSFT shares. Overall, market sentiment is mixed, but potential buyers should weigh the pros and cons before making a decision, as the stock's future trajectory remains uncertain.

**Amazon (AMZN):**
Today's Closing Price: $201.13
Change Percent: -3.47%
News Summary: Amazon stock has been named a "Top Pick" by Evercore ISI, signaling optimism about its future performance. Despite tariffs weighing on e-commerce stocks, analysts see Amazon as better positioned than its competitors. The company is also making strides in the quantum computing revolution, which could potentially boost its stock price. With Amazon dropping into oversold territory for the first time in 7 months, investors may see this as a buying opportunity. Ahead of the Alexa+ launch, market sentiment remains cautious, but overall, Amazon's strong positioning and innovative endeavors could positively impact its stock price.

**Alphabet (GOOGL):**
Today's Closing Price: $172.59
Change Percent: -0.25%
News Summary: Alphabet's stock fell 17% in February, but the company remains a potential "millionaire maker" stock. Google has called on the Justice Department to keep the company intact, indicating a strong stance against potential breakups. Despite this, the stock has dipped into oversold territory, joining the likes of Tesla and Amazon. However, Eagle Capital Management has identified Alphabet as a stock to buy, suggesting a potential rebound. With market sentiment being mixed, investors should be cautious, but also watch for potential buying opportunities, as the company's strong fundamentals and innovative products could drive future growth.

**Meta (META):**
Today's Closing Price: $632.82
Change Percent: -3.60%
News Summary: Meta stock has caught the attention of analysts and investors alike, with many considering it a bargain despite a recent winning streak interruption. Two key factors contributed to the break in the streak: ad revenue concerns and increased competition. However, with the stock appearing cheap and its promising growth prospects, investors are weighing the potential benefits of buying in. Notably, Jim Cramer's trust has sold some Meta shares amid the bull run, but the stock remains a top pick for 2025, with it being the only "Magnificent 7" stock currently shining. Overall, market sentiment is cautiously optimistic, with investors advised to keep a close eye on Meta's performance and potential buying opportunities.

**Nvidia (NVDA):**
Today's Closing Price: $111.47
Change Percent: -4.97%
News Summary: Nvidia is poised to make significant gains in 2025, driven by promising developments. The company's stock is anticipated to soar, thanks to key announcements from CEO Jensen Huang. With a potential race to a $5 trillion valuation, Nvidia is competing with tech giant Apple. Preliminary market movements show Nvidia's stock on the rise, potentially signaling a perceived bargain. However, billionaire investor Stanley Druckenmiller has recently divested his Nvidia shares, opting for alternative AI investments. Overall, market sentiment remains optimistic, with many expecting Nvidia to make substantial strides in the AI sector, potentially impacting its stock price positively.

**Tesla (TSLA):**
Today's Closing Price: $263.80
Change Percent: -5.48%
News Summary: Tesla's stock has plummeted due to declining sales in Europe and a warning from an analyst. Despite this, Morgan Stanley still considers it a top pick. However, Baird has labeled it a bearish fresh pick, and Elon Musk's involvement in right-wing politics may deter car buyers and negatively impact the stock. With market sentiment being bearish, investors should be cautious, but also watch for potential buying opportunities as the company navigates these challenges.

Stay tuned for more updates.

- **The Magnificent Seven Insider**
```
