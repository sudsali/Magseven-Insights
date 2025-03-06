from agents import StockDataAgent, NewsAgent, SummaryAgent, SummaryEditorAgent
from tasks import fetch_news_task, generate_newsletter
from tools import generate_company_update
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

def main():
    print("Gathering latest news on the Magnificent Seven stocks...\n")

    all_updates = []
    for company, symbol in [
        ("Apple", "AAPL"),
        ("Microsoft", "MSFT"),
        ("Amazon", "AMZN"),
        ("Alphabet", "GOOGL"),
        ("Meta", "META"),
        ("Nvidia", "NVDA"),
        ("Tesla", "TSLA")
    ]:
        try:
            company_update = generate_company_update(company, symbol)
            if company_update:
                all_updates.append(company_update)
        except Exception as e:
            print(f"Error generating update for {company}: {e}")

    try:
        newsletter_content = generate_newsletter(all_updates)
        editor_agent = SummaryEditorAgent()
        refined_newsletter = editor_agent.remove_extra_summary(newsletter_content)

        print(refined_newsletter)
    except Exception as e:
        print(f"Error generating newsletter: {e}")

if __name__ == "__main__":
    main()