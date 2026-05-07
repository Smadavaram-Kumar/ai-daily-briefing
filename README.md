# AI Daily Briefing

A command-line tool that fetches your morning briefing — weather + top news headlines — and saves a history.

## Features
- 🌤️ Current weather via OpenWeatherMap
- 📰 Top headlines via NewsAPI
- 💾 Auto-saves history to `data/history.json`

## Setup

1. Clone the repo:
```bash
   git clone https://github.com/Smadavaram-Kumar/ai-daily-briefing.git
   cd ai-daily-briefing
```

2. Create and activate a virtual environment:
```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1   # Windows PowerShell
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Get free API keys:
   - OpenWeatherMap: https://openweathermap.org/api
   - NewsAPI: https://newsapi.org

5. Copy `.env.example` to `.env` and fill in your keys:
```bash
   copy .env.example .env
```

6. Run it:
```bash
   python main.py
```

## Tech
- Python 3.12
- requests (HTTP client)
- python-dotenv (secrets management)