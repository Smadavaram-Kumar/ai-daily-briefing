"""
news.py
Handles all NewsAPI interactions.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"


def get_top_headlines(country: str = "us", limit: int = 5) -> list:
    """
    Fetch top news headlines for a country.
    Returns a list of dicts with title, source, url.
    """
    if not API_KEY:
        raise ValueError("NEWSAPI_KEY not set in .env file")

    try:
        response = requests.get(
            BASE_URL,
            params={
                "country": country,
                "pageSize": limit
            },
            headers={"X-Api-Key": API_KEY},   # Key in HEADER (more secure)
            timeout=10
        )
        print("raw : ", response.raise_for_status())
        raw = response.json()
        print("raw : ", raw)
        # Clean the response into just what we need
        articles = []
        for article in raw.get("articles", []):
            articles.append({
                "title": article.get("title", "No title"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url", ""),
            })
        return articles

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid NewsAPI key")
        elif e.response.status_code == 429:
            raise ValueError("NewsAPI rate limit hit (100/day on free tier)")
        raise

    except requests.exceptions.Timeout:
        raise TimeoutError("NewsAPI request timed out")