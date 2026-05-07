"""
main.py
Daily Briefing — runs the whole show.
"""
import os
import json
from datetime import datetime
from dotenv import load_dotenv

from weather import get_weather
from news import get_top_headlines

load_dotenv()

DEFAULT_CITY = os.getenv("DEFAULT_CITY", "London")
NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "us")
HISTORY_FILE = "data/history.json"


def print_weather(weather: dict) -> None:
    """Pretty-print the weather block."""
    print("\n" + "=" * 50)
    print(f"🌤️  WEATHER — {weather['city']}, {weather['country']}")
    print("=" * 50)
    print(f"  Condition:    {weather['description']}")
    print(f"  Temperature:  {weather['temp']}°C (feels like {weather['feels_like']}°C)")
    print(f"  Humidity:     {weather['humidity']}%")
    print(f"  Wind speed:   {weather['wind_speed']} m/s")


def print_news(articles: list) -> None:
    """Pretty-print the news block."""
    print("\n" + "=" * 50)
    print("📰 TOP HEADLINES")
    print("=" * 50)
    for i, article in enumerate(articles, start=1):
        print(f"  {i}. {article['title']}")
        print(f"     ↳ {article['source']}")
        print(f"     {article['url']}\n")


def save_history(weather: dict, articles: list) -> None:
    """Append today's briefing to history.json."""
    os.makedirs("data", exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "weather": weather,
        "news": articles
    }

    # Load existing history (if any)
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved briefing to {HISTORY_FILE}")


def main():
    print(f"\n📅 Daily Briefing — {datetime.now().strftime('%A, %B %d, %Y')}")

    # Step 1: Fetch weather
    try:
        weather = get_weather(DEFAULT_CITY)
        print(weather)
        print_weather(weather)
    except Exception as e:
        print(f"\n❌ Weather failed: {e}")
        weather = None

    # Step 2: Fetch news
    try:
        articles = get_top_headlines(country=NEWS_COUNTRY, limit=5)
        print(articles)
        print_news(articles)
    except Exception as e:
        print(f"\n❌ News failed: {e}")
        articles = []

    # Step 3: Save (only if at least one succeeded)
    if weather or articles:
        save_history(weather or {}, articles)

    print("\n✅ Done.\n")


if __name__ == "__main__":
    main()