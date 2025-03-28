import requests
import datetime
import config  # Import API key from config.py

NEWS_API_KEY = config.NEWS_API_KEY  # Ensure you have this in config.py
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(company_name, num_articles=20):
    """
    Fetches news articles related to a given company for the last 7 days.
    
    Args:
        company_name (str): Name of the company.
        num_articles (int): Number of news articles to fetch.
    
    Returns:
        list: A list of news articles (each as a dictionary).
    """
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=7)  # Last 7 days

    params = {
        "q": company_name,
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d"),
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": num_articles,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("articles", [])  # Extract only articles
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

# Test function
if __name__ == "__main__":
    articles = fetch_news("Microsoft")
    print(f"Fetched {len(articles)} articles.")
